import io, codecs
import json
from typing import Any, Dict, Optional, cast

import yaml
from modelbit.api import JobApi, MbApi
from modelbit.error import UserFacingError
from modelbit.helpers import getDeploymentName
from modelbit.internal.load import loadFromPickle
from modelbit.internal.s3 import getS3FileBytes
from modelbit.internal.secure_storage import DownloadableObjectInfo, getSecureData
from modelbit.utils import inDeployment


def getJobOutputFromWeb(mbApi: MbApi,
                        branch: str,
                        runtimeName: str,
                        jobName: str,
                        userFacingId: Optional[int] = None,
                        fileName: Optional[str] = None,
                        modelName: Optional[str] = None,
                        restoreClass: Optional[type] = None):
  data = JobApi(mbApi).getJobOutputContent(branch=branch,
                                           runtimeName=runtimeName,
                                           jobName=jobName,
                                           userFacingId=userFacingId,
                                           fileName=fileName,
                                           modelName=modelName)
  if data is None:
    raise UserFacingError(f"Couldn't find {jobName}'s {modelName or fileName or 'default output'}")
  elif isinstance(data, str):
    return data
  return _downloadJobOutputFromEncObjInfo(modelName if modelName else fileName or 'data.pkl', data,
                                          restoreClass)


def _downloadJobOutputFromEncObjInfo(key: str,
                                     data: DownloadableObjectInfo,
                                     restoreClass: Optional[type] = None):
  objBytes = getSecureData(data, key)
  if key.endswith(".pkl"):
    return loadFromPickle(objBytes, restoreClass)
  else:
    try:
      return codecs.decode(objBytes)  # try returning a text file
    except UnicodeDecodeError:
      return objBytes


def getJobOutputFromDeployment(branch: str,
                               runtimeName: str,
                               jobName: str,
                               userFacingId: Optional[int] = None,
                               fileName: Optional[str] = None,
                               modelName: Optional[str] = None,
                               restoreClass: Optional[type] = None) -> Any:
  assert inDeployment()
  if modelName:
    return _getJobOutputRegistryModelFromS3(branch, runtimeName, jobName, userFacingId, modelName,
                                            restoreClass)

  if fileName is None:
    fileName = f"data/{jobName}.pkl"
  if userFacingId is None and runtimeName == getDeploymentName():
    return _getJobOutputFromLocalFile(fileName=fileName, restoreClass=restoreClass)
  return _getJobOutputFromS3(branch, runtimeName, jobName, userFacingId, fileName, restoreClass)


def _getJobOutputFromLocalFile(fileName: str, restoreClass: Optional[type] = None):
  with open(fileName, 'rb') as f:
    runtimeObjBytes = f.read()
    assert runtimeObjBytes is not None
    return loadFromPickle(runtimeObjBytes, restoreClass)


def _getJobOutputRegistryModelFromS3(branch: str,
                                     runtimeName: str,
                                     jobName: str,
                                     userFacingId: Optional[int] = None,
                                     modelName: Optional[str] = None,
                                     restoreClass: Optional[type] = None):

  if modelName is None:
    return None

  jobRunAlias = str(userFacingId) if userFacingId is not None else branch

  s3Path = f"jobs/{runtimeName}/{jobName}/{jobRunAlias}/registry.json.zstd.enc"
  registryBytes = getS3FileBytes(s3Path)
  if registryBytes is None:
    raise UserFacingError(f"Could not find file {s3Path}")

  registry = json.loads(registryBytes.decode())
  modelData = registry.get(modelName)
  if modelData is None:
    return None

  contentHash = cast(Optional[str], modelData.get('contentHash'))
  runtimeObjBytes = getS3FileBytes(f"runtime_objects/{contentHash}.zstd.enc")
  assert runtimeObjBytes is not None
  return loadFromPickle(runtimeObjBytes, restoreClass)


def _getJobOutputFromS3(branch: str,
                        runtimeName: str,
                        jobName: str,
                        userFacingId: Optional[int] = None,
                        fileName: Optional[str] = None,
                        restoreClass: Optional[type] = None):
  jobRunAlias = str(userFacingId) if userFacingId is not None else branch

  s3Path = f"jobs/{runtimeName}/{jobName}/{jobRunAlias}/repo/{fileName}.zstd.enc"
  fileStubBytes = getS3FileBytes(s3Path)
  if fileStubBytes is None:
    raise UserFacingError(f"Could not find file {s3Path}")

  yamlData = cast(Dict[str, Any], yaml.load(io.BytesIO(fileStubBytes), Loader=yaml.SafeLoader))

  contentHash = cast(Optional[str], yamlData["contentHash"])
  runtimeObjBytes = getS3FileBytes(f"runtime_objects/{contentHash}.zstd.enc")
  assert runtimeObjBytes is not None
  return loadFromPickle(runtimeObjBytes, restoreClass)
