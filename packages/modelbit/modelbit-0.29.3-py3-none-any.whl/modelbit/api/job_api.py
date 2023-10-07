import logging
from typing import Any, Dict, List, Optional, Union

from modelbit.internal.secure_storage import DownloadableObjectInfo

from .api import MbApi
from .object_api import EncryptedObjectInfo

logger = logging.getLogger(__name__)


class JobDesc:
  jobName: str

  runtimeName: Optional[str]
  branch: Optional[str]
  command: Union[str, List[str], None]
  schedule: Optional[str]
  emailOnFailure: Optional[str]
  refreshDatasets: Optional[List[str]]
  size: Optional[str]
  saveOnSuccess: Optional[bool]
  timeoutMinutes: Optional[int]
  arguments: Optional[List[str]]

  def __init__(self, data: Dict[str, Any]):
    self.jobName = data["jobName"]
    self.runtimeName = data.get("runtimeName", None)
    self.branch = data.get("branch", None)

    self.command = data.get("command", None)
    self.schedule = data.get("schedule", None)
    self.emailOnFailure = data.get("emailOnFailure", None)
    self.refreshDatasets = data.get("refreshDatasets", None)
    self.size = data.get("size", None)
    self.saveOnSuccess = data.get("saveOnSuccess", None)
    self.timeoutMinutes = data.get("timeoutMinutes", None)
    self.arguments = data.get("arguments", None)

  def __repr__(self):
    return str(self.__dict__)


# Similar to RecentJobInfo
class JobRunDesc:
  id: str
  userFacingId: int
  jobName: str
  state: str
  finishedAtMs: Optional[int] = None
  startedAtMs: Optional[int] = None
  errorMessage: Optional[str]
  successMessage: Optional[str]
  newRuntimeVersion: Optional[str]
  runtimeName: str
  jobOverviewUrl: Optional[str]

  def __init__(self, data: Dict[str, Any]):
    self.id = data["id"]
    self.userFacingId = data["userFacingId"]
    self.jobName = data["jobName"]
    self.runtimeName = data["runtimeName"]
    self.state = data["state"]
    if "finishedAtMs" in data:
      self.finishedAtMs = int(data["finishedAtMs"])
    if "startedAtMs" in data:
      self.startedAtMs = int(data["startedAtMs"])
    self.errorMessage = data.get("errorMessage", None)
    self.successMessage = data.get("successMessage", None)
    self.newRuntimeVersion = data.get("newRuntimeVersion", None)
    self.jobOverviewUrl = data.get("jobOverviewUrl", None)

  def __repr__(self):
    return str(self.__dict__)


class JobApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def getJobRun(self, jobId: str) -> JobRunDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/jobs/run_info", dict(jobId=jobId))
    return JobRunDesc(resp["jobRun"])

  def runJob(self,
             branch: str,
             runtimeName: str,
             jobName: str,
             args: Optional[List[Any]] = None) -> JobRunDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/jobs/run_job",
                                   dict(runtimeName=runtimeName, branch=branch, jobName=jobName, args=args))
    return JobRunDesc(resp["jobRun"])

  def getJobOutputContent(self,
                          branch: str,
                          runtimeName: str,
                          jobName: str,
                          userFacingId: Optional[int] = None,
                          fileName: Optional[str] = None,
                          modelName: Optional[str] = None) -> Optional[Union[str, DownloadableObjectInfo]]:
    resp = self.api.getJsonOrThrow(
        "api/cli/v1/jobs/get_output_content",
        dict(branch=branch,
             runtimeName=runtimeName,
             jobName=jobName,
             userFacingId=userFacingId,
             fileName=fileName,
             modelName=modelName))
    if "encryptedObjectInfo" in resp:
      return EncryptedObjectInfo(resp["encryptedObjectInfo"])
    if "content" in resp:
      return resp["content"]
    return None
