__version__ = "0.30.0"
__author__ = 'Modelbit'
from . import helpers as m_helpers

m_helpers.pkgVersion = __version__

import os, sys, yaml, pickle, logging
from typing import cast, Union, Callable, Any, Dict, List, Optional, TYPE_CHECKING

# aliasing since some of these overlap with functions we want to expose to users

from . import runtime as m_runtime
from . import utils as m_utils
from . import model_wrappers as m_model_wrappers
from . import collect_dependencies as m_collect_dependencies
from . import jobs as m_jobs
from . import telemetry as m_telemetry

from modelbit.internal.auth import mbApi as _mbApi, mbApiReadOnly, isAuthenticated as isAuthenticated
from modelbit.error import ModelbitError as ModelbitError, UserFacingError as UserFacingError

if TYPE_CHECKING:
  import pandas
  import modelbit.internal.datasets as m_datasets
  import modelbit.internal.warehouses as m_warehouses
  import modelbit.internal.deployments as m_deployments

m_telemetry.initLogging()
logger = logging.getLogger(__name__)


# Nicer UX for customers: from modelbit import Deployment
class Deployment(m_runtime.Deployment):
  ...


errorHandler = lambda msg: m_telemetry.eatErrorAndLog(mbApiReadOnly(), msg)  # type: ignore


def __str__():
  return "Modelbit Client"


def _repr_html_():  # type: ignore
  return ""


@errorHandler("Failed to add models.")
def add_models(models: Dict[str, Any]):
  """
  https://doc.modelbit.com/api-reference/add_models
  """
  if m_utils.inDeployment() and not m_utils.inRuntimeJob():
    raise UserFacingError("mb.add_models is not supported within deployments")

  import modelbit.internal.registry as m_registry
  m_registry.set_many(_mbApi(), models)


@errorHandler("Failed to add model.")
def add_model(name: str, model: Any):
  """
  https://doc.modelbit.com/api-reference/add_model
  """
  if m_utils.inDeployment() and not m_utils.inRuntimeJob():
    raise UserFacingError("mb.add_model is not supported within deployments")

  import modelbit.internal.registry as m_registry
  m_registry.set(_mbApi(), name, model)


@errorHandler("Failed to get model.")
def get_model(name: str):
  """
  https://doc.modelbit.com/api-reference/get_model
  """
  import modelbit.internal.registry as m_registry
  return m_registry.get(_mbApi(), name)


@errorHandler("Failed to list models.")
def models(prefix: Optional[str] = None):
  """
  https://doc.modelbit.com/api-reference/models
  """
  import modelbit.internal.registry as m_registry
  return m_registry.list_names(_mbApi(), prefix)


@errorHandler("Failed to delete model.")
def delete_models(names: Union[str, List[str]]):
  """
  https://doc.modelbit.com/api-reference/delete_models
  """
  if m_utils.inDeployment():
    raise UserFacingError("mb.delete_models is not supported within deployments")
  import modelbit.internal.registry as m_registry
  return m_registry.delete(_mbApi(), names)


@errorHandler("Failed to add job.")
def add_job(
    func: Callable[..., Any],
    deployment_name: str,
    name: Optional[str] = None,
    store_result_as: Optional[str] = None,
    python_version: Optional[str] = None,
    python_packages: Optional[List[str]] = None,
    system_packages: Optional[List[str]] = None,
    extra_files: Union[str, List[str], Dict[str, str], None] = None,
    skip_extra_files_dependencies: bool = False,
    redeploy_on_success: Optional[bool] = None,
    save_on_success: bool = True,
    email_on_failure: Optional[str] = None,
    schedule: Optional[str] = None,
    refresh_datasets: Optional[List[str]] = None,
    size: Optional[str] = None,
    timeout_minutes: Optional[int] = None,
    default_arguments: Optional[List[Any]] = None,
) -> 'm_jobs.ModelbitJobWrapper':
  """
  https://doc.modelbit.com/api-reference/add_job
  """
  if redeploy_on_success is not None:
    print("Warning: redeploy_on_success is deprecated. Use save_on_success instead")
    save_on_success = redeploy_on_success
  return m_jobs.add_job(_mbApi(),
                        func,
                        deployment_name,
                        name=name,
                        store_result_as=store_result_as,
                        python_version=python_version,
                        python_packages=python_packages,
                        system_packages=system_packages,
                        extra_files=extra_files,
                        skip_extra_files_dependencies=skip_extra_files_dependencies,
                        save_on_success=save_on_success,
                        email_on_failure=email_on_failure,
                        schedule=schedule,
                        refresh_datasets=refresh_datasets,
                        size=size,
                        timeout_minutes=timeout_minutes,
                        default_arguments=default_arguments)


@errorHandler("Failed to run job.")
def run_job(deployment_name: str,
            job_name: Optional[str] = None,
            arguments: Optional[List[Any]] = None,
            branch: Optional[str] = None) -> 'm_jobs.ModelbitJobRun':
  """
  https://doc.modelbit.com/api-reference/run_job
  """
  if type(deployment_name) is str and job_name is not None:
    return m_jobs.runJob(runtimeName=deployment_name,
                         jobName=job_name,
                         args=arguments,
                         mbApi=_mbApi(),
                         branch=branch or m_helpers.getCurrentBranch())
  else:
    raise TypeError("missing job_name")


@errorHandler("Failed to get job output.")
def get_job_output(deployment_name: str,
                   job_name: str,
                   branch: Optional[str] = None,
                   run_id: Optional[int] = None,
                   result_stored_as: Optional[str] = None,
                   file_name: Optional[str] = None,
                   model_name: Optional[str] = None):
  """
  https://doc.modelbit.com/api-reference/get_job_output
  """
  if result_stored_as is not None:
    file_name = f"data/{result_stored_as}.pkl"
  return m_jobs.getJobOutput(runtimeName=deployment_name,
                             jobName=job_name,
                             branch=branch or m_helpers.getCurrentBranch(),
                             userFacingId=run_id,
                             fileName=file_name,
                             modelName=model_name,
                             mbApi=_mbApi())


@errorHandler("Failed to list datasets.")
def datasets() -> 'm_datasets.DatasetList':
  """
  https://doc.modelbit.com/api-reference/datasets
  """
  import modelbit.internal.datasets as m_datasets
  return m_datasets.list(_mbApi())


@errorHandler("Failed to load dataset.")
def get_dataset(dsName: str,
                filters: Optional[Dict[str, List[Any]]] = None,
                filter_column: Optional[str] = None,
                filter_values: Optional[List[Any]] = None,
                optimize: Optional[bool] = None,
                legacy: Optional[bool] = None,
                branch: Optional[str] = None) -> Optional['pandas.DataFrame']:
  """
  https://doc.modelbit.com/api-reference/get_dataset
  """
  if filter_column is not None and filter_values is not None:
    print("Deprecated: filter_column= & filter_values= will be removed soon. Use filters= instead.")
    if filters is None:
      filters = {}
    filters[filter_column] = filter_values
  if optimize is not None:
    print("Deprecated: optimize= will be removed soon.")

  import modelbit.internal.feature_store as m_feature_store
  return m_feature_store.getDataFrame(_mbApi(),
                                      branch=branch or m_helpers.getCurrentBranch(),
                                      dsName=dsName,
                                      filters=filters)


@errorHandler("Failed to load warehouses.")
def warehouses() -> 'm_warehouses.WarehousesList':
  """
  https://doc.modelbit.com/api-reference/warehouses
  """
  import modelbit.internal.warehouses as m_warehouses
  return m_warehouses.list(_mbApi())


@errorHandler("Failed to load deployments.")
def deployments() -> 'm_deployments.DeploymentsList':
  import modelbit.internal.deployments as m_deployments
  return m_deployments.list(_mbApi())


@errorHandler("Failed to add files.")
def add_files(deployment: str,
              files: Union[str, List[str], Dict[str, str]],
              modelbit_file_prefix: Optional[str] = None,
              strip_input_path: Optional[bool] = False):
  """
  https://doc.modelbit.com/api-reference/add_files
  """
  return m_runtime.add_files(_mbApi(), deployment, files, modelbit_file_prefix, strip_input_path)


@errorHandler("Failed to add objects.")
def add_objects(deployment: str, values: Dict[str, Any]):
  return m_runtime.add_objects(_mbApi(), deployment, values)


@errorHandler("Failed to load secret.")
def get_secret(name: str,
               deployment: Optional[str] = None,
               branch: Optional[str] = None,
               encoding: str = "utf8") -> str:
  """
  https://doc.modelbit.com/api-reference/get_secret
  """
  import modelbit.internal.secrets as m_secrets
  return m_secrets.get_secret(name, deployment, branch, encoding, _mbApi())


@errorHandler("Failed to add package.")
def add_package(path: str, force: bool = False):
  """
  https://doc.modelbit.com/api-reference/add_package
  """
  import modelbit.internal.package as m_package
  return m_package.add_package(path, force, _mbApi())


@errorHandler("Failed to delete package.")
def delete_package(name: str, version: str):
  import modelbit.internal.package as m_package
  return m_package.delete_package(name, version, _mbApi())


@errorHandler("Failed to add common files.")
def add_common_files(files: Union[List[str], Dict[str, str], str]):
  """
  https://doc.modelbit.com/api-reference/add_common_files
  """
  import modelbit.internal.common_files as m_common_files
  m_common_files.addFiles(_mbApi(), files)


@errorHandler("Failed to delete common files.")
def delete_common_files(names: Union[List[str], str]):
  """
  https://doc.modelbit.com/api-reference/delete_common_files
  """
  import modelbit.internal.common_files as m_common_files
  m_common_files.deleteFiles(_mbApi(), names)


@errorHandler("Failed to list common files.")
def common_files(prefix: Optional[str] = None):
  """
  https://doc.modelbit.com/api-reference/common_files
  """
  import modelbit.internal.common_files as m_common_files
  return m_common_files.listFiles(_mbApi(), prefix)


@errorHandler("Failed to deploy.")
def deploy(deployableObj: Union[Callable[..., Any], 'm_runtime.Deployment'],
           name: Optional[str] = None,
           python_version: Optional[str] = None,
           python_packages: Optional[List[str]] = None,
           system_packages: Optional[List[str]] = None,
           dataframe_mode: bool = False,
           example_dataframe: Optional['pandas.DataFrame'] = None,
           extra_files: Union[str, List[str], Dict[str, str], None] = None,
           skip_extra_files_dependencies: bool = False,
           require_gpu: bool = False):
  """
  https://doc.modelbit.com/api-reference/deploy
  """
  if type(deployableObj) is m_jobs.ModelbitJobWrapper:
    raise UserFacingError("Cannot deploy a job. Use modelbit.add_job()")

  if _objIsDeployment(deployableObj):
    deployableObj = cast(Deployment, deployableObj)
    return deployableObj.deploy()
  elif callable(deployableObj) and deployableObj.__name__ == "<lambda>":
    if isinstance(extra_files, str):
      extra_files = [extra_files]
    return m_model_wrappers.LambdaWrapper(deployableObj,
                                          name=name,
                                          python_version=python_version,
                                          python_packages=python_packages,
                                          system_packages=system_packages,
                                          dataframe_mode=dataframe_mode,
                                          example_dataframe=example_dataframe,
                                          extra_files=extra_files,
                                          skip_extra_files_dependencies=skip_extra_files_dependencies,
                                          require_gpu=require_gpu).makeDeployment(_mbApi()).deploy()
  elif callable(deployableObj):
    return Deployment(api=_mbApi(),
                      name=name,
                      deploy_function=deployableObj,
                      python_version=python_version,
                      python_packages=python_packages,
                      system_packages=system_packages,
                      dataframe_mode=dataframe_mode,
                      example_dataframe=example_dataframe,
                      extra_files=extra_files,
                      skip_extra_files_dependencies=skip_extra_files_dependencies,
                      require_gpu=require_gpu).deploy()
  elif hasattr(deployableObj, "__module__") and "sklearn" in deployableObj.__module__ and hasattr(
      deployableObj, "predict"):
    if isinstance(extra_files, str):
      extra_files = [extra_files]
    return m_model_wrappers.SklearnPredictor(deployableObj,
                                             name=name,
                                             python_version=python_version,
                                             python_packages=python_packages,
                                             system_packages=system_packages,
                                             dataframe_mode=dataframe_mode,
                                             example_dataframe=example_dataframe,
                                             extra_files=extra_files,
                                             skip_extra_files_dependencies=skip_extra_files_dependencies,
                                             require_gpu=require_gpu).makeDeployment(_mbApi()).deploy()
  else:
    raise Exception("First argument must be a function or Deployment object.")


@errorHandler("Unable to log in.")
def login(region: Optional[str] = None, branch: Optional[str] = None):
  """
  https://doc.modelbit.com/api-reference/login
  """
  _mbApi(region=region, branch=branch)
  return sys.modules['modelbit']


def switch_branch(branch: str):
  """
  https://doc.modelbit.com/api-reference/switch_branch
  """
  # See if new branch exists, but not from deployments
  if (not m_utils.inDeployment() and not mbApiReadOnly().refreshAuthentication(branch=branch)):
    raise UserFacingError(f"Branch {branch} not found.")
  m_helpers.setCurrentBranch(branch)


def get_branch() -> str:
  """
  https://doc.modelbit.com/api-reference/get_branch
  """
  return m_helpers.getCurrentBranch()


def in_modelbit() -> bool:
  """
  https://doc.modelbit.com/api-reference/in_modelbit
  """
  return m_utils.inDeployment()


def get_deployment_info() -> Dict[str, Any]:
  """
  https://doc.modelbit.com/api-reference/get_deployment_info
  """
  if not in_modelbit():
    print("get_deployment_info: Warning, not currently running in a deployment.")
  return {
      "branch": m_helpers.getCurrentBranch(),
      "name": m_helpers.getDeploymentName(),
      "version": m_helpers.getDeploymentVersion()
  }


def log_image(obj: Any):
  """
  https://doc.modelbit.com/api-reference/log_image
  """
  import modelbit.file_logging as m_file_logging
  m_file_logging.logImage(obj)


def load_value(name: str, restoreClass: Optional[type] = None):
  if name.endswith(".pkl"):
    import __main__ as main_package
    # Support finding files relative to source location
    # This doesn't work from lambda, so only use when not in a deployment
    if not os.path.exists(name):
      name = os.path.join(os.path.dirname(main_package.__file__), name)

    with open(name, "rb") as f:
      value = pickle.load(f)
      if restoreClass is not None and isinstance(value, m_helpers.InstancePickleWrapper):
        return value.restore(restoreClass)
      else:
        return value
  extractPath = os.environ['MB_EXTRACT_PATH']
  objPath = os.environ['MB_RUNTIME_OBJ_DIR']
  if not extractPath or not objPath:
    raise Exception("Missing extractPath/objPath")
  with open(f"{extractPath}/metadata.yaml", "r") as f:
    yamlData = cast(Dict[str, Any], yaml.load(f, Loader=yaml.SafeLoader))  # type: ignore
  data: Dict[str, Dict[str, str]] = yamlData["data"]
  contentHash = data[name]["contentHash"]
  with open(f"{objPath}/{contentHash}.pkl.gz", "rb") as f:
    return m_utils.deserializeGzip(contentHash, f.read)


def save_value(obj: Any, filepath: str):
  if not m_collect_dependencies.savedSpecialObj(obj, filepath):
    if not os.path.exists(os.path.dirname(filepath)):
      os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if (hasattr(obj, "__module__") and obj.__module__ == "__main__"):
      # If the object is in __main__, move it so we can load it from a source file.
      # This allows objects saved from jobs to be loaded by inference functions.
      import inspect
      callerFrame = inspect.stack()[1]
      module = inspect.getmodule(callerFrame[0])
      if module is not None and module.__file__ is not None:
        obj = m_utils.repickleFromMain(obj, module)

    with open(filepath, "wb") as f:
      pickle.dump(obj, f)


def _objIsDeployment(obj: Any):
  try:
    if type(obj) in [Deployment, m_runtime.Deployment]:
      return True
    # catch modelbit._reload() class differences
    if obj.__class__.__name__ in ['Deployment']:
      return True
  except:
    return False
  return False


def parseArg(s: str) -> Any:
  import json
  try:
    return json.loads(s)
  except json.decoder.JSONDecodeError:
    return s
