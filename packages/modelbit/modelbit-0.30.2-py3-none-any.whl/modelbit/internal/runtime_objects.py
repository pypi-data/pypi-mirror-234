import logging, os, glob
from typing import Any, Optional, Union, List, Dict

from modelbit.api import MbApi, ObjectApi
from modelbit.internal.secure_storage import getSecureData, putSecureData
from modelbit.internal.retry import retry
from modelbit.internal.describe import calcHash, describeFile, describeObject, shouldUploadFile
from modelbit.internal.file_stubs import toYaml
from modelbit.error import UserFacingError

logger = logging.getLogger(__name__)

MAX_FOUND_FILES = 1000  # prevent mistakes where folks upload a zillion files by accident


@retry(8, logger)
def uploadRuntimeObject(api: MbApi,
                        objData: bytes,
                        contentHash: str,
                        uxDesc: str,
                        showLoader: bool = True) -> None:
  resp = ObjectApi(api).runtimeObjectUploadInfo(contentHash)
  putSecureData(resp, objData, uxDesc, showLoader)
  return None


@retry(8, logger)
def downloadRuntimeObject(api: MbApi, contentHash: str, desc: str) -> Union[bytes, memoryview]:
  resp = ObjectApi(api).runtimeObjectDownloadUrl(contentHash)
  if not resp or not resp.objectExists:
    raise Exception("Failed to get file URL")
  data = getSecureData(resp, desc)
  if not data:
    raise Exception(f"Failed to download and decrypt")
  return data


def describeAndUploadRuntimeObject(api: MbApi, obj: Optional[Any], objData: bytes, uxDesc: str) -> str:
  contentHash = calcHash(objData)
  if obj is None:
    description = describeFile(objData, 1)
  else:
    description = describeObject(obj, 1)
  yamlObj = toYaml(contentHash, len(objData), description)
  uploadRuntimeObject(api, objData, contentHash, uxDesc)
  return yamlObj


def expandDirs(files: Union[str, List[str], Dict[str, str], None]) -> Dict[str, str]:
  if files is None:
    return {}

  if isinstance(files, str):
    files = [files]

  if isinstance(files, List):
    files = {path: path for path in files}

  newFiles: Dict[str, str] = {}
  for fLocal, fRemote in files.items():
    if os.path.isdir(fLocal):
      fileList = glob.glob(os.path.join(fLocal, "**"), recursive=True)
      if len(fileList) > MAX_FOUND_FILES:
        raise UserFacingError(
            f"Aborting: {len(fileList)} files found under {fLocal} which may be a mistake. Recursive file discovery limited to {MAX_FOUND_FILES} files."
        )
      for f in fileList:
        if os.path.isdir(f):
          continue
        if "__pycache__" in f:
          continue
        newFiles[f] = os.path.join(fRemote, os.path.relpath(f, fLocal))
    else:
      newFiles[fLocal] = fRemote
  return newFiles


def prepareFileList(api: MbApi,
                    files: Union[str, List[str], Dict[str, str], None],
                    modelbit_file_prefix: Optional[str] = None,
                    strip_input_path: Optional[bool] = False) -> Dict[str, str]:
  dataFiles: Dict[str, str] = {}
  for [localFilepath, modelbitFilepath] in expandDirs(files).items():
    if strip_input_path:
      modelbitFilepath = os.path.basename(modelbitFilepath)
    if modelbit_file_prefix is not None:
      modelbitFilepath = os.path.join(modelbit_file_prefix, modelbitFilepath)
    try:
      with open(localFilepath, "rb") as f:
        data = f.read()
        if shouldUploadFile(localFilepath, data):
          uploadResult = describeAndUploadRuntimeObject(api, None, data, localFilepath)
          if uploadResult:
            dataFiles[modelbitFilepath] = uploadResult
        else:
          dataFiles[modelbitFilepath] = data.decode("utf8") or "\n"
    except FileNotFoundError:
      raise UserFacingError(f"File not found: {localFilepath}")
  return dataFiles
