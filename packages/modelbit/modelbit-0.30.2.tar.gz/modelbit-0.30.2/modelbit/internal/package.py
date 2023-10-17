import hashlib
import logging
import os
import re
import shutil
import stat
import tarfile
import tempfile
import zipfile
from contextlib import contextmanager
from typing import Any, Iterator, List, Optional, Tuple

import build
import build.env
import build.util
import pkginfo
from modelbit.api import MbApi, PackageApi, PackageDescResponse
from modelbit.internal.file_stubs import toYaml
from modelbit.internal.runtime_objects import uploadRuntimeObject
from modelbit.telemetry import UserFacingError
from modelbit.utils import timeago
from modelbit.ux import printTemplate

logger = logging.getLogger(__name__)


class PackageInfo:
  name: str
  version: str

  def __init__(self, name: str, version: str):
    self.name = name
    self.version = version

  def __repr__(self):
    return f"{self.name}=={self.version}"


def list_packages(name: Optional[str], api: MbApi):
  return PackageApi(api).fetchPackageList(name)


def add_package(path: str, force: bool, api: MbApi) -> Optional[PackageInfo]:
  builder = PackageBuilder(api)
  pkgKind, pkgInfo = builder.packageInfo(path)
  printTemplate("package-uploading", None, pkgInfo=pkgInfo, path=os.path.abspath(path))
  pkgInfo = builder.buildAndUploadPackage(path, force, (pkgKind, pkgInfo))
  printTemplate("package-uploaded", None, pkgInfo=pkgInfo)
  return pkgInfo


def delete_package(name: str, version: str, api: MbApi) -> Optional[PackageDescResponse]:
  if "==" in name and not version:
    name, version = name.split("==")
  resp = PackageApi(api).deletePackage(name, version)
  if resp is None:
    raise UserFacingError(f"Package {name}=={version} not found")
  printTemplate("package-deleted", None, name=name, version=version)
  return resp


class PackageBuilder:

  def __init__(self, api: MbApi):
    self.api = api

  def packageInfo(self, path: str) -> Tuple[str, PackageInfo]:
    stat_res = os.stat(path)
    if stat.S_ISDIR(stat_res.st_mode):
      pkgInfo = _pkgMetadata(path)
      if pkgInfo:
        return "packagedir", pkgInfo
      else:
        pkgName = normalizePkgName(os.path.basename(os.path.abspath(path)))
        pkgInfo, _ = self.fetchNextPackageVersion(pkgName)
        return "rawdir", pkgInfo
    elif _pathIsSDist(path):
      sDistInfo = pkginfo.SDist(path)
      return "sdist", PackageInfo(name=normalizePkgName(sDistInfo.name), version=sDistInfo.version)
    elif _pathIsWheel(path):
      wheelInfo = pkginfo.Wheel(path)
      return "wheel", PackageInfo(name=normalizePkgName(wheelInfo.name), version=wheelInfo.version)
    else:
      raise Exception(f"Unknown filetype {os.path.splitext(path)[-1]}")

  def buildAndUploadPackage(self,
                            path: str,
                            allowClobberVersions: bool,
                            pkgKindInfo: Optional[Tuple[str, PackageInfo]] = None) -> PackageInfo:
    wheelPath, pkgInfo, recordHash = self.buildPackage(path, allowClobberVersions, pkgKindInfo)
    return self.uploadPackage(wheelPath, allowClobberVersions, pkgInfo, recordHash)

  def buildPackage(self,
                   path: str,
                   allowClobberVersions: bool,
                   pkgKindInfo: Optional[Tuple[str, PackageInfo]] = None) -> Tuple[str, PackageInfo, str]:
    wheelPath: str
    pkgKind, pkgInfo = pkgKindInfo or self.packageInfo(path)

    self._validatePackageInfo(pkgInfo, allowClobberVersions)
    if pkgKind == "packagedir":
      wheelPath = _buildViaSdist(path)
    elif pkgKind == "sdist":
      wheelPath = _buildViaSdist(path)  # Convert sdist to wheel
    elif pkgKind == "wheel":
      wheelPath = path
    elif pkgKind == "rawdir":
      with _temporaryProjectFolder(path, pkgInfo) as path:
        wheelPath = _buildViaSdist(path)
    else:
      raise Exception("Unknown package kind")

    recordHash = self._getWheelRecordHash(wheelPath)
    return wheelPath, pkgInfo, recordHash

  # The name of the .dist-info file may not be normalized, but we often only know the normalized name. So
  # we search for the record file instead of looking it up by name
  def _getWheelRecordHash(self, wheelPath: str) -> str:
    with zipfile.ZipFile(wheelPath) as archive:
      pythonFiles = [f.orig_filename for f in archive.filelist if f.orig_filename.endswith(".py")]
      if len(pythonFiles) == 0:
        raise UserFacingError("Invalid package: no .py files were found.")
      for file in archive.filelist:
        if file.orig_filename.endswith(".dist-info/RECORD"):
          record = archive.read(file.orig_filename)
          record = re.sub(b"(?m)^.+\\.dist-info.*$", b"", record).strip()
          return f"sha1:{hashlib.sha1(record).hexdigest()}"
    raise Exception(f"Could not find .dist-info in {wheelPath}")

  def uploadPackage(self, wheelPath: str, allowClobberVersions: bool, pkgInfo: PackageInfo,
                    recordHash: str) -> PackageInfo:
    with open(wheelPath, 'rb') as f:
      content = f.read()
      contentHash = f"sha1:{hashlib.sha1(content).hexdigest()}"
    uploadRuntimeObject(self.api, content, contentHash, f"packages/{os.path.basename(wheelPath)}")

    metadata = {"recordHash": recordHash}
    yamlContent = toYaml(contentHash, len(content), metadata)
    PackageApi(self.api).uploadPackage(pkgInfo.name, pkgInfo.version, yamlContent, allowClobberVersions)
    return pkgInfo

  def _validatePackageInfo(self, pkgInfo: PackageInfo, allowClobberVersions: bool) -> None:
    fetchedPkgDesc = PackageApi(self.api).fetchPackageDesc(pkgInfo.name, pkgInfo.version)
    if fetchedPkgDesc is None or allowClobberVersions:
      return
    raise UserFacingError(
        f"Package {fetchedPkgDesc.name}=={fetchedPkgDesc.version} already uploaded {timeago(fetchedPkgDesc.createdAtMs or 0)}"
    )

  def fetchNextPackageVersion(self, name: str) -> Tuple[PackageInfo, Optional[PackageDescResponse]]:
    name = normalizePkgName(name)
    pkgInfo = PackageApi(self.api).fetchPackageDesc(name, None)
    nextVersion = _nextSemVer(pkgInfo.version) if pkgInfo is not None and pkgInfo.version else "0.0.1"
    if nextVersion is None:
      raise Exception(f"Unable to create next package semver for package {name} from {str(pkgInfo)}")
    return (PackageInfo(name=name, version=nextVersion), pkgInfo)


def _pkgMetadata(path: str) -> Optional[PackageInfo]:
  try:
    metadata = build.util.project_wheel_metadata(path, isolated=False)

    return PackageInfo(name=normalizePkgName(metadata["Name"]), version=metadata["Version"])
  except build.BuildException:
    return None


def _genSetupPy(pkgInfo: PackageInfo) -> str:
  return f"""from setuptools import setup, find_packages
setup(
    name='{pkgInfo.name}',
    version='{pkgInfo.version}',
    packages=find_packages(),
)"""


# # This cannot be used until we deprecate python3.6 but it is the future
# def _genProjectToml(pkgInfo: PackageInfo) -> str:
#   return f"""[project]
# name = "{pkgInfo.name}"
# version = "{pkgInfo.version}"
# """


# Copies the project into a properly named sub-folder so pip will install properly
# Create a temporary project setupPy so we can set the version and name
# Creates an __init__.py it none exists as it's required for a project
# Without these, you cannot import files the same as you do in a notebook
@contextmanager
def _temporaryProjectFolder(path: str, pkgInfo: PackageInfo) -> Iterator[str]:
  tmpdir = tempfile.mkdtemp('modelbit')

  def ignoreHiddenFiles(dirName: str, dirFileNames: List[str]) -> List[str]:
    ignoreList: List[str] = []
    if dirName.startswith("."):
      ignoreList.append(dirName)
    for fileName in dirFileNames:
      if fileName.startswith("."):
        ignoreList.append(dirName)
    return ignoreList

  try:
    pkgdir = os.path.join(tmpdir, pkgInfo.name)
    shutil.copytree(path, pkgdir, ignore=ignoreHiddenFiles)
    logger.info("Not a python project, creating temporary setup.py")
    setupPyPath = os.path.join(tmpdir, "setup.py")
    handle = os.open(setupPyPath, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(handle, 'w') as file_obj:
      file_obj.write(_genSetupPy(pkgInfo))
    initPyPath = os.path.join(pkgdir, "__init__.py")
    if not os.path.exists(initPyPath):
      open(initPyPath, "w").close()
    yield tmpdir
  finally:
    shutil.rmtree(tmpdir)


class QuietBuilder(build.ProjectBuilder):

  def __init__(self, *args: Any, **kwargs: Any):
    try:
      import pyproject_hooks
      kwargs["runner"] = pyproject_hooks.quiet_subprocess_runner  # type: ignore
    except:
      pass

    super().__init__(*args, **kwargs)

  @staticmethod
  def log(message: str):
    logger.info(message)


class QuietEnvBuilder(build.env.IsolatedEnvBuilder):

  def __init__(self, *args: Any, **kwargs: Any):
    super().__init__(*args, **kwargs)

  @staticmethod
  def log(message: str):
    logger.info(message)


# We build via sdist to ensure the wheel is built clean
def _buildViaSdist(path: str) -> str:
  shouldDeleteSdist = False
  if path.endswith(".tar.gz"):  # Is sdist
    sdist = path
  else:
    sdist = _build(path, "sdist")  # Build the sdist
    shouldDeleteSdist = True
  sdist_name = os.path.basename(sdist)
  sdist_out = tempfile.mkdtemp(prefix='build-via-sdist-')
  with tarfile.open(sdist) as t:
    t.extractall(sdist_out)
    try:
      return _build(os.path.join(sdist_out, sdist_name[:-len('.tar.gz')]), "wheel")
    finally:
      shutil.rmtree(sdist_out, ignore_errors=True)
      if shouldDeleteSdist:
        os.unlink(sdist)


def _build(path: str, kind: str) -> str:
  outdir = os.path.join(tempfile.gettempdir(), 'modelbit')
  with QuietEnvBuilder() as env:
    builder = QuietBuilder(path, python_executable=env.executable, scripts_dir=env.scripts_dir)

    # first install the build dependencies
    env.install(builder.build_system_requires)
    # then get the extra required dependencies from the backend
    env.install(builder.get_requires_for_build(kind))
    return builder.build(kind, outdir, {})


simpleSemVer = re.compile(
    r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
)
onlyNumbers = re.compile('[^0-9]+')


def _nextSemVer(version: str) -> Optional[str]:
  m = simpleSemVer.match(version)
  if not m:
    return None
  parts = [int(onlyNumbers.sub("", v)) for v in m.groups() if v is not None]
  parts[-1] += 1
  return ".".join(str(p) for p in parts)


def _pathIsSDist(path: str) -> bool:
  return path.endswith(".tar.gz")


def _pathIsWheel(path: str) -> bool:
  return path.endswith(".whl")


def normalizePkgName(name: str):
  return re.sub(r"[-_.]+", "-", name).lower()
