import time
from typing import Any, Callable, Dict, List, Optional, Union, cast

from modelbit.api import JobApi, JobDesc, JobRunDesc, MbApi
from modelbit.error import UserFacingError
from modelbit.internal.runtime_jobs import getJobOutputFromDeployment, getJobOutputFromWeb
from modelbit.model_wrappers import RuntimeJobWrapper
from modelbit.utils import inDeployment
from modelbit.ux import printTemplate, renderTemplate


def add_job(
    api: MbApi,
    func: Callable[..., Any],
    deployment_name: str,
    name: Optional[str] = None,
    store_result_as: Optional[str] = None,
    python_version: Optional[str] = None,
    python_packages: Optional[List[str]] = None,
    system_packages: Optional[List[str]] = None,
    extra_files: Union[str, List[str], Dict[str, str], None] = None,
    save_on_success: bool = True,
    email_on_failure: Optional[str] = None,
    skip_extra_files_dependencies: bool = False,
    schedule: Optional[str] = None,
    refresh_datasets: Optional[List[str]] = None,
    size: Optional[str] = None,
    timeout_minutes: Optional[int] = None,
    default_arguments: Optional[List[Any]] = None,
):
  if not callable(func):
    raise UserFacingError("First argument must be a function")

  if func.__name__ == "source":  # avoid collisions with source.py
    raise UserFacingError("The job function cannot be named 'source'")

  if type(save_on_success) is not bool:
    raise UserFacingError("The save_on_success parameter must be a boolean")

  if email_on_failure is not None and type(email_on_failure) is not str:
    raise UserFacingError("The email_on_failure parameter must be a string")

  if schedule is not None and type(schedule) is not str:
    raise UserFacingError("The schedule parameter must be a string")

  if refresh_datasets is not None and type(refresh_datasets) is not list:
    raise UserFacingError("The refresh_datasets parameter must be a list of strings")

  if size is not None and size not in [
      "small", "medium", "large", "xlarge", "2xlarge", "4xlarge", "gpu_small", "gpu_medium", "gpu_large"
  ]:
    raise UserFacingError(
        'The size parameter must be one of "small", "medium", "large", "xlarge", "2xlarge", "4xlarge", "gpu_small", "gpu_medium", or "gpu_large"'
    )

  if timeout_minutes is not None and (type(timeout_minutes) is not int or timeout_minutes <= 0):
    raise UserFacingError("The timeout_minutes parameter must be a positive integer")

  if default_arguments is not None:
    assertArgsAreSerializable(*default_arguments)

  name = name or func.__name__
  store_result_as = store_result_as or name
  jobDesc = dict(jobName=name,
                 schedule=schedule,
                 saveOnSuccess=save_on_success,
                 emailOnFailure=email_on_failure,
                 refreshDatasets=refresh_datasets,
                 timeoutMinutes=timeout_minutes,
                 runtimeName=deployment_name,
                 size=size,
                 arguments=default_arguments)
  job = ModelbitJobWrapper(func, jobDesc, store_result_as)
  deployment = RuntimeJobWrapper(
      job,
      name=deployment_name,
      python_version=python_version,
      python_packages=python_packages,
      system_packages=system_packages,
      extra_files=extra_files,
      skip_extra_files_dependencies=skip_extra_files_dependencies,
  ).makeDeployment(api)

  deployment.deploy()
  return job


def runJob(
    mbApi: MbApi,
    branch: str,
    runtimeName: str,
    jobName: str,
    args: Optional[List[Any]],
) -> 'ModelbitJobRun':
  if args is not None:
    assertArgsAreSerializable(*args)
  jobRunDesc = JobApi(mbApi).runJob(branch, runtimeName, jobName, args)
  printTemplate("running-job", None, jobName=jobName, jobOverviewUrl=jobRunDesc.jobOverviewUrl)
  return ModelbitJobRun(mbApi, jobRunDesc)


# TODO: cache results
def getJobOutput(mbApi: MbApi,
                 branch: str,
                 runtimeName: str,
                 jobName: str,
                 userFacingId: Optional[int] = None,
                 fileName: Optional[str] = None,
                 modelName: Optional[str] = None,
                 restoreClass: Optional[type] = None):
  if inDeployment():
    return getJobOutputFromDeployment(branch=branch,
                                      runtimeName=runtimeName,
                                      jobName=jobName,
                                      userFacingId=userFacingId,
                                      fileName=fileName,
                                      modelName=modelName,
                                      restoreClass=restoreClass)
  else:
    return getJobOutputFromWeb(mbApi,
                               branch=branch,
                               runtimeName=runtimeName,
                               jobName=jobName,
                               userFacingId=userFacingId,
                               fileName=fileName,
                               modelName=modelName,
                               restoreClass=restoreClass)


def assertArgsAreSerializable(*args: List[Any]) -> None:
  import json
  try:
    json.dumps(args)
  except TypeError:
    raise UserFacingError("Default arguments must be a list of JSON serializable objects")


class ModelbitJobRun:
  _jobRunId: str
  _api: MbApi
  _desc: Optional[JobRunDesc]

  @property
  def deployment_name(self):
    return self._desc.runtimeName if self._desc is not None else None

  @property
  def job_name(self):
    return self._desc.jobName if self._desc is not None else None

  @property
  def run_id(self):
    return self._desc.userFacingId if self._desc is not None else None

  def __init__(self, mbApi: MbApi, jobRunId: Union[str, 'JobRunDesc']):
    self._api = mbApi
    if type(jobRunId) is str:
      self._jobRunId = jobRunId
      self._desc = None
    else:
      self._desc = cast(JobRunDesc, jobRunId)
      self._jobRunId = self._desc.id

  def __repr__(self) -> str:
    if self._desc is not None:
      return f"<ModelbitJobRun: run_id={self._desc.userFacingId}>"
    return f"<ModelbitJobRun>"

  def refresh(self) -> 'ModelbitJobRun':
    self._desc = JobApi(self._api).getJobRun(self._jobRunId)
    return self

  def wait(self, timeout_sec: Optional[int] = None, quiet: bool = True):
    deadline = time.time() + timeout_sec if timeout_sec is not None else None
    while deadline is None or time.time() < deadline:
      self.refresh()
      if not quiet:
        print(self._desc)
      if self._desc is None or self._desc.state == "failed":
        raise UserFacingError("Job failed.")
      elif self._desc.state == "finished":
        return
      sleepTime = min(20, max(0, deadline - time.time())) if deadline is not None else 20
      time.sleep(sleepTime)
    raise TimeoutError("Job still running")


class ModelbitJobWrapper:
  desc: JobDesc
  storeResultAs: str

  def __init__(self, func: Callable[..., Any], desc: Union[JobDesc, Dict[str, Any]], storeResultAs: str):
    self.func = func
    self.desc = desc if type(desc) is JobDesc else JobDesc(cast(Dict[str, Any], desc))
    self.storeResultAs = storeResultAs

  def _repr_html_(self):
    return self.__repr__()

  def __repr__(self):
    return renderTemplate("job", jobName=self.desc.jobName, deploymentName=self.desc.runtimeName)
