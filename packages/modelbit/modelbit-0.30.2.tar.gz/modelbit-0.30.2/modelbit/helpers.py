import logging
import os, re
from typing import Any, Dict, List, Optional, Tuple, cast, Set

from .environment import listMissingPackagesFromImports, listMissingPackagesFromPipList, listLocalModulesFromImports, listInstalledPackageNames, packagesToIgnoreFromImportCheck, versionProbablyWrong, listInstalledPackages
from .utils import branchFromEnv, inRuntimeJob
from .ux import MismatchedPackageWarning, MissingPackageFromImportWarning, MissingExtraFileWarning, WarningErrorTip, ProbablyNotAPackageWarning, ProbablyWantDataframeModeWarning, ProbablyVersionWrong, MissingModelDeps

pkgVersion: str = ""  # set in __init__
_currentBranch = branchFromEnv() if inRuntimeJob() else "main"
defaultRequestTimeout = 10

logger = logging.getLogger(__name__)


class RuntimePythonProps:
  excludeFromDict: List[str] = ['errors']

  def __init__(self):
    self.source: Optional[str] = None
    self.name: Optional[str] = None
    self.argNames: Optional[List[str]] = None
    self.argTypes: Optional[Dict[str, str]] = None
    self.namespaceVarsDesc: Optional[Dict[str, str]] = None
    self.namespaceFunctions: Optional[Dict[str, str]] = None
    self.namespaceImports: Optional[Dict[str, str]] = None
    self.namespaceFroms: Optional[Dict[str, str]] = None
    self.namespaceModules: Optional[List[str]] = None
    self.errors: Optional[List[str]] = None
    self.namespaceVars: Optional[Dict[str, Any]] = None
    self.namespaceConstants: Optional[Dict[str, str]] = None
    self.customInitCode: Optional[List[str]] = None
    self.extraDataFiles: Optional[Dict[str, Tuple[Any, bytes]]] = None
    self.extraSourceFiles: Optional[Dict[str, str]] = None
    self.job: Optional[JobProps] = None
    self.userClasses: List[str] = []
    self.functionsCallingGetModelButNoModels: List[str] = []


class JobProps:

  def __init__(self, name: str, storeResultAs: str, rtProps: RuntimePythonProps, schedule: Optional[str],
               saveOnSuccess: bool, emailOnFailure: Optional[str], refreshDatasets: Optional[List[str]],
               size: Optional[str], timeoutMinutes: Optional[int], arguments: Optional[List[str]]):
    self.name = name
    self.outVar = storeResultAs
    self.rtProps = rtProps
    self.schedule = schedule
    self.saveOnSuccess = saveOnSuccess
    self.emailOnFailure = emailOnFailure
    self.refreshDatasets = refreshDatasets
    self.size = size
    self.timeoutMinutes = timeoutMinutes
    self.arguments = arguments


# For instances of user defined classes. Default Pickle doesn't handle unpickling user defined
# classes because they cannot be imported, since they're defined in the notebook
class InstancePickleWrapper:

  def __init__(self, obj: Any):
    self.clsName = obj.__class__.__name__
    self.mbClassForStub = obj.__class__.__name__
    self.mbModuleForStub = obj.__class__.__module__
    if hasattr(obj, "__getstate__"):
      self.state = obj.__getstate__()
    else:
      self.state = obj.__dict__
    self.desc = str(obj)
    if self.desc.startswith("<__main"):
      self.desc = str(self.state)

  def __repr__(self) -> str:
    return self.desc

  def restore(self, restoreClass: type):
    inst = cast(Any, restoreClass.__new__(restoreClass))  # type: ignore
    if hasattr(inst, "__setstate__"):
      inst.__setstate__(self.state)
    else:
      inst.__dict__ = self.state
    return inst


def getMissingPackageWarningsFromEnvironment(pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromPipList(pyPackages)
  if len(missingPackages) > 0:
    for mp in missingPackages:
      desiredPackage, similarPackage = mp
      if similarPackage is not None:
        warnings.append(MismatchedPackageWarning(desiredPackage, similarPackage))
  return warnings


def getMissingPackageWarningsFromImportedModules(importedModules: Optional[List[str]],
                                                 pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromImports(importedModules, pyPackages)
  for mp in missingPackages:
    importedModule, pipPackageInstalled = mp
    warnings.append(MissingPackageFromImportWarning(importedModule, pipPackageInstalled))
  return warnings


def getMissingLocalFileWarningsFromImportedModules(
    importedModules: Optional[List[str]], extraFiles: Dict[str, str]) -> List[MissingExtraFileWarning]:
  warnings: List[MissingExtraFileWarning] = []
  localModules = listLocalModulesFromImports(importedModules)
  for lm in localModules:
    missing = True
    for filePath in extraFiles.keys():
      if lm in filePath:  # using string match for simple v1
        missing = False
    if lm == "modelbit":  # modelbit isn't "installed" in dev mode, so it doesn't show in
      missing = False
    if missing:
      warnings.append(MissingExtraFileWarning(lm))
  return warnings


def getProbablyNotAPackageWarnings(pyPackages: Optional[List[str]]) -> List[ProbablyNotAPackageWarning]:
  if pyPackages is None or len(pyPackages) == 0:
    return []
  ignorablePackages = packagesToIgnoreFromImportCheck(pyPackages)
  warnings: List[ProbablyNotAPackageWarning] = []
  installedPackages = set([p.lower() for p in listInstalledPackageNames()])
  for packageWithVersion in pyPackages:
    if packageWithVersion.lower().startswith(("git+", "http")) or "[" in packageWithVersion:
      continue
    nameOnly = re.split("[=<>]+", packageWithVersion)[0]
    if nameOnly in ignorablePackages:
      continue
    if nameOnly.lower() not in installedPackages:
      warnings.append(ProbablyNotAPackageWarning(nameOnly))
  return warnings


def warningIfShouldBeUsingDataFrameWarning(
    argNames: Optional[List[str]], argTypes: Optional[Dict[str,
                                                           str]]) -> List[ProbablyWantDataframeModeWarning]:
  if argNames is None or len(argNames) != 1 or argTypes is None:
    return []
  if argTypes.get(argNames[0], None) == "DataFrame":
    return [ProbablyWantDataframeModeWarning()]
  return []


def getVersionProbablyWrongWarnings(pyPackages: Optional[List[str]]) -> List[ProbablyVersionWrong]:
  if pyPackages is None or len(pyPackages) == 0:
    return []

  installedPackages = listInstalledPackages()

  warnings: List[ProbablyVersionWrong] = []
  for pkg in pyPackages:
    if pkg in installedPackages:
      continue
    try:
      if versionProbablyWrong(pkg):
        warnings.append(ProbablyVersionWrong(pkg))
    except Exception as err:
      logger.info("Error checking versionProbablyWrong: %s", err)
  return warnings


def getMissingModelDepsWarning(missingCalls: List[str]) -> MissingModelDeps:
  return MissingModelDeps(", ".join(missingCalls))


def setCurrentBranch(branch: str):
  global _currentBranch
  if type(branch) != str:
    raise Exception("Branch must be a string.")
  if (branch != _currentBranch):
    logger.info("Changing branch to %s", branch)
  # oldBranch = _currentBranch
  _currentBranch = branch
  # if isAuthenticated() and not _refreshAuthentication():
  #   logger.info("Auth failed, reverting to %s", oldBranch)
  #   _currentBranch = oldBranch


def getCurrentBranch():
  global _currentBranch
  return _currentBranch


def getDeploymentName() -> Optional[str]:
  return os.environ.get('DEPLOYMENT_NAME')


def getDeploymentVersion() -> Optional[str]:
  return os.environ.get('DEPLOYMENT_VERSION')


def mergePipPackageLists(usersList: List[str], inferredList: List[str]) -> List[str]:
  mergedList: List[str] = []
  seenPackageNames: Set[str] = set()
  for pkg in (usersList + inferredList):
    if pkg.startswith("git+https"):
      mergedList.append(pkg)
    else:
      nameOnly = re.split("[=<>]+", pkg)[0]
      if nameOnly not in seenPackageNames:
        seenPackageNames.add(nameOnly)
        mergedList.append(pkg)
  mergedList.sort()
  return mergedList
