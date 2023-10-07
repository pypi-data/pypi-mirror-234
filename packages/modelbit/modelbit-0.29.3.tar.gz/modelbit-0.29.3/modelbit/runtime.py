from enum import Enum
from typing import Union, List, Dict, Any, Callable, Tuple, Optional, cast, TYPE_CHECKING
import re, json

from .environment import ALLOWED_PY_VERSIONS, getInstalledPythonVersion, listMissingPackagesFromImports, systemPackagesForPips, scrubUnwantedPackages, addDependentPackages, annotateSpecialPackages
from .helpers import RuntimePythonProps, getCurrentBranch, getMissingPackageWarningsFromEnvironment, getMissingPackageWarningsFromImportedModules, getProbablyNotAPackageWarnings, warningIfShouldBeUsingDataFrameWarning, mergePipPackageLists, pkgVersion, getVersionProbablyWrongWarnings, getMissingModelDepsWarning
from .ux import COLORS, DifferentPythonVerWarning, GenericError, WarningErrorTip, makeCssStyle, TableHeader, printTemplate, renderTemplate
from .collect_dependencies import getFuncSource, getRuntimePythonProps, getFuncArgNames, tryPickle
from .source_generation import makeSourceFile, makeCreateJobRequest, DefaultModuleName
from .utils import guessNotebookType, guessOs
from .error import UserFacingError
import logging

from modelbit.api import DeployedRuntimeDesc, MbApi, RuntimeApi, DeploymentTestDesc, BranchApi
from modelbit.internal import runtime_objects
from modelbit.internal.registry import resetRecentlyUsedModels
from modelbit.internal.auth import mbApi
if TYPE_CHECKING:
  import pandas
  import modelbit.jobs as m_jobs

logger = logging.getLogger(__name__)


class DeploymentTestError(Enum):
  UnknownFormat = 'UnknownFormat'
  ExpectedNotJson = 'ExpectedNotJson'
  CannotParseArgs = 'CannotParseArgs'


# a bit of a hack for now
def _parseTimeFromDeployMessage(message: Optional[str]):
  if not message:
    return None
  if "will be ready in" in message:
    return message.split("will be ready in")[1]
  return None


class RuntimeStatusNotes:

  def __init__(self, tips: List[WarningErrorTip], warnings: List[WarningErrorTip],
               errors: List[WarningErrorTip]):
    self.tips = tips
    self.warnings = warnings
    self.errors = errors
    self.deployable = len(errors) == 0

  def statusMsg(self):
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self):
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class Runtime:

  def __init__(self,
               api: MbApi,
               name: Optional[str] = None,
               main_function: Optional[Callable[..., Any]] = None,
               python_version: Optional[str] = None,
               requirements_txt_filepath: Optional[str] = None,
               requirements_txt_contents: Optional[List[str]] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               docker_run: Optional[str] = None,
               source_override: Optional[str] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               extra_files: Union[str, List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               job: Optional['m_jobs.ModelbitJobWrapper'] = None,
               require_gpu: bool = False):

    self._pythonPackages: Optional[List[str]] = None
    self._systemPackages: Optional[List[str]] = None
    self._dockerRun: Optional[str] = None
    self._deployName: Optional[str] = None
    self._deployFunc: Optional[Callable[..., Any]] = None
    self._sourceOverride = source_override
    self._testOutputs: List[Tuple[bool, DeploymentTestDesc, Dict[str, str]]] = []
    self._dataframeMode = dataframe_mode
    self._dataframe_mode_columns: Optional[List[Dict[str, str]]] = None
    self._deploymentInfo: Optional[DeployedRuntimeDesc] = None

    self._require_gpu = require_gpu
    self._extraFiles = extra_files
    self._ignoreExtraFilesDependencies = skip_extra_files_dependencies
    self._pythonVersion = getInstalledPythonVersion()
    self._job = job
    self._api = api

    if name:
      self.set_name(name)
    if main_function:
      self._set_main_function(main_function)
    if python_version:
      self.set_python_version(python_version)
    if requirements_txt_filepath:
      self.set_requirements_txt(filepath=requirements_txt_filepath)
    if requirements_txt_contents:
      self.set_requirements_txt(contents=requirements_txt_contents)
    if python_packages is not None:
      self.set_python_packages(python_packages)
    if system_packages is not None:
      self.set_system_packages(system_packages)
    if docker_run:
      self._set_docker_run(docker_run)

    if dataframe_mode and example_dataframe is not None:
      self._dataframe_mode_columns = self._collectDataFrameModeColumns(example_dataframe)
    elif dataframe_mode and example_dataframe is None:
      raise UserFacingError("The example_dataframe parameter is required when passing dataframe_mode=True")
    elif not dataframe_mode and example_dataframe is not None:
      raise UserFacingError(
          "Setting dataframe_mode=True is required when passing the example_dataframe parameter")

  def _repr_html_(self):
    return self.__repr__()

  def __repr__(self):
    if self._deployName is None:
      return ""
    elif self._deploymentInfo is None:
      return renderTemplate("deployment", name=self._deployName, version=None)
    else:
      return renderTemplate("deployment", name=self._deployName, version=self._deploymentInfo.version)

  def get_version(self):
    if self._deploymentInfo is None:
      raise UserFacingError("Call .deploy() to create a version.")
    return self._deploymentInfo.version

  def set_name(self, name: str):
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise UserFacingError("Names should be alphanumeric with underscores.")
    self._deployName = name
    return self

  def set_python_version(self, version: str):
    if version not in ALLOWED_PY_VERSIONS:
      return self._selfError(f'Python version should be one of {ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version
    return self

  def set_requirements_txt(self, filepath: Optional[str] = None, contents: Optional[List[str]] = None):
    lines: List[str] = []
    if filepath != None and type(filepath) == str:
      f = open(filepath, "r")
      lines = [n.strip() for n in f.readlines()]
      return self.set_python_packages(lines)
    elif contents != None:
      return self.set_python_packages(contents)
    return self

  def set_python_packages(self, packages: Optional[List[str]]):
    if packages is None:
      self._pythonPackages = None
      return
    if type(packages) != list:
      raise UserFacingError("The python_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise UserFacingError("The python_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise UserFacingError("The python_packages parameters cannot contain newlines")
      if "==" not in pkg and not pkg.startswith("https") and not pkg.startswith("git+https"):
        raise UserFacingError(
            f"The python_packages parameter '{pkg}' is formatted incorrectly. It should look like 'package-name==X.Y.Z'"
        )
    self._pythonPackages = sorted(packages)

  def set_system_packages(self, packages: Optional[List[str]]):
    if packages is None:
      self._systemPackages = None
      return
    if type(packages) != list:
      raise UserFacingError("The system_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise UserFacingError("The system_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise UserFacingError("The system_packages parameters cannot contain newlines.")
    self._systemPackages = sorted(packages)

  def _set_docker_run(self, commands: Optional[str]):
    if commands is None:
      self._dockerRun = None
      return
    if type(commands) != str:
      raise UserFacingError("The docker_run parameter must be a string.")
    if "\n" in commands or "\r" in commands:
      raise UserFacingError("The docker_run parameter cannot contain newlines.")
    self._dockerRun = commands

  def _set_main_function(self, func: Callable[..., Any]):
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.set_name(func.__name__)
    tests = self._getTests()
    if tests == None:
      self._testOutputs = []
    elif len(tests) > 0 and self._dataframeMode:
      raise UserFacingError("Unit tests are not supported in dataframe_mode")
    else:
      self._testOutputs = self._getTestOutputs(tests)
    return self

  def _getRequirementsTxt(self):
    if self._pythonPackages:
      packages = "\n".join(self._pythonPackages)
      if "jax[" in packages:
        packages = "--find-links=https://storage.googleapis.com/jax-releases/jax_cuda_releases.html\n" + packages
      if "torch==" in packages or "torchvision==" in packages:
        packages = "--extra-index-url=https://download.pytorch.org/whl/\n" + packages
      return packages
    else:
      return None

  def _getRuntimePythonProps(self):
    props: Optional[RuntimePythonProps] = None
    error: Optional[GenericError] = None

    try:
      localExtraFiles: Optional[List[str]] = list(runtime_objects.expandDirs(self._extraFiles).keys())
      if self._ignoreExtraFilesDependencies:
        localExtraFiles = None
      props = getRuntimePythonProps(self._deployFunc,
                                    sourceOverride=self._sourceOverride,
                                    job=self._job,
                                    extraFiles=localExtraFiles)
    except TypeError:
      raise
    except Exception as err:
      error = GenericError(str(err))
    return props, error

  def deploy(self):
    self._decideAllPackages()
    deployKind = "runtime" if self._deployFunc is not None else "runtime-job"

    status = self._getStatusNotes()
    if not status.deployable:
      logger.info("Unable to deploy: %s", status.errors)
      printTemplate("runtime-notes",
                    None,
                    deploymentName=self._deployName,
                    warningsList=status.warnings,
                    tipsList=status.tips,
                    errorsList=status.errors)
      self._describeHtml()
      return self

    printTemplate(f"{deployKind}-deploying",
                  None,
                  deploymentName=self._deployName,
                  jobName=self._job.desc.jobName if self._job is not None else None,
                  warningsList=status.warnings,
                  tipsList=status.tips,
                  errorsList=status.errors)

    rtProps, error = self._getRuntimePythonProps()
    if error is not None or rtProps is None:
      printTemplate("error", None, errorText="Unable to continue because errors are present.")
      return self

    BranchApi(self._api).raiseIfProtected()

    sourceFile = makeSourceFile(rtProps, DefaultModuleName).asDict() if self._deployFunc is not None else None

    dataFiles = self._makeAndUploadDataFiles(rtProps)
    createRuntimeRequest: Dict[str, Any] = {
        "name": self._deployName,
        "dataFiles": dataFiles,
        "pyState": {
            "sourceFile": sourceFile,
            "valueFiles": {},
            "name": rtProps.name,
            "module": DefaultModuleName,
            "argNames": rtProps.argNames,
            "argTypes": rtProps.argTypes,
            "requirementsTxt": self._getRequirementsTxt(),
            "pythonVersion": self._pythonVersion,
            "systemPackages": self._systemPackages,
            "dockerRun": self._dockerRun,
            "dataframeModeColumns": self._dataframe_mode_columns,
        },
        "job": makeCreateJobRequest(rtProps.job) if rtProps.job is not None else None,
        "source": {
            "os": guessOs(),
            "kind": guessNotebookType(),
            "version": pkgVersion
        },
    }
    if self._require_gpu:
      createRuntimeRequest['pyState']['capabilities'] = ['gpu']
    if len(json.dumps(createRuntimeRequest)) > 5_000_000:
      raise UserFacingError("Request size exceeds maximum allowed (5MB).")

    resp = RuntimeApi(self._api).createRuntime(getCurrentBranch(), createRuntimeRequest)
    self._deploymentInfo = resp
    jobName = self._job.desc.jobName if self._job is not None else None
    printTemplate(f"{deployKind}-deployed",
                  None,
                  deploymentName=self._deployName,
                  deployMessage=resp.message,
                  jobName=jobName,
                  deployTimeWords=_parseTimeFromDeployMessage(resp.message),
                  runtimeOverviewUrl=resp.runtimeOverviewUrl)
    resetRecentlyUsedModels()
    return None

  def _makeAndUploadDataFiles(self, pyState: RuntimePythonProps):
    dataFiles: Dict[str, str] = {}
    if pyState.namespaceVars:
      for nName, nVal in pyState.namespaceVars.items():
        uploadResult = runtime_objects.describeAndUploadRuntimeObject(self._api, nVal, tryPickle(nVal, nName),
                                                                      nName)
        if uploadResult:
          dataFiles[f"data/{nName.lower()}.pkl"] = uploadResult
    if pyState.extraDataFiles is not None:
      for nName, nObjBytes in pyState.extraDataFiles.items():
        uploadResult = runtime_objects.describeAndUploadRuntimeObject(self._api, nObjBytes[0], nObjBytes[1],
                                                                      nName)
        if uploadResult:
          dataFiles[f"data/{nName.lower()}.pkl"] = uploadResult
    if pyState.extraSourceFiles:
      dataFiles.update(pyState.extraSourceFiles)
    dataFiles.update(runtime_objects.prepareFileList(self._api, self._extraFiles))
    if pyState.job is not None:
      dataFiles.update(self._makeAndUploadDataFiles(pyState.job.rtProps))
    return dataFiles

  def _selfError(self, txt: str):
    printTemplate("error", None, errorText=txt)
    return None

  def _describeHtml(self):
    customStyles = {
        "readyStyle": makeCssStyle({"color": COLORS["success"]}),
        "errorStyle": makeCssStyle({"color": COLORS["error"]}),
        "passStyle": makeCssStyle({
            "color": COLORS["success"],
            "font-weight": "bold"
        }),
        "failStyle": makeCssStyle({
            "color": COLORS["error"],
            "font-weight": "bold"
        }),
    }
    status = self._getStatusNotes()
    funcProps, error = self._getRuntimePythonProps()
    if funcProps is None:
      return renderTemplate(
          "error",
          errorText=f"Unable to capture deployment function. {error.errorText if error is not None else ''}")

    propHeaders = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, isCode=True),
    ]
    propRows: List[List[str]] = []

    funcSig = '(None)'
    if funcProps.name and funcProps.argNames:
      funcSig = f"{funcProps.name}({', '.join(funcProps.argNames)})"
    propRows.append(["Function", funcSig])

    if funcProps.namespaceFunctions and len(funcProps.namespaceFunctions) > 0:
      nsFuncs = "\n".join([k for k, _ in funcProps.namespaceFunctions.items()])
      propRows.append(["Helpers", nsFuncs])

    if funcProps.namespaceVarsDesc and len(funcProps.namespaceVarsDesc) > 0:
      nsVars = "\n".join([f'{k}: {v}' for k, v in funcProps.namespaceVarsDesc.items()])
      propRows.append(["Values", nsVars])

    nsImports: List[str] = []
    if funcProps.namespaceFroms and len(funcProps.namespaceFroms) > 0:
      for k, v in funcProps.namespaceFroms.items():
        nsImports.append(f'from {v} import {k}')
    if funcProps.namespaceImports and len(funcProps.namespaceImports) > 0:
      for k, v in funcProps.namespaceImports.items():
        nsImports.append(f'import {v} as {k}')
    if len(nsImports) > 0:
      propRows.append(["Imports", '\n'.join(nsImports)])

    propRows.append(["Python Version", self._pythonVersion])

    if self._pythonPackages and len(self._pythonPackages) > 0:
      maxDepsShown = 7
      if len(self._pythonPackages) > maxDepsShown:
        deps = "\n".join([d for d in self._pythonPackages[:maxDepsShown]])
        numLeft = len(self._pythonPackages) - maxDepsShown
        deps += f'\n...and {numLeft} more.'
      else:
        deps = "\n".join([d for d in self._pythonPackages])
      propRows.append(["Python packages", deps])

    if self._systemPackages:
      propRows.append(["System packages", ", ".join(self._systemPackages)])

    if self._dockerRun:
      propRows.append(["Docker RUN", self._dockerRun])

    testHeaders = [
        TableHeader("Status", TableHeader.LEFT, isPassFail=True),
        TableHeader("Command", TableHeader.LEFT, isCode=True),
        TableHeader("Result", TableHeader.LEFT, isCode=True),
    ]
    testRows: List[List[Union[str, bool]]] = []
    for tOut in self._testOutputs:
      result: List[str] = []
      metadata = tOut[2]
      if "error" in metadata:
        result.append(f'Error: {metadata["error"]}')
      if "expected" in metadata:
        result.append(f'Expected: {metadata["expected"]}')
      if "received" in metadata:
        result.append(f'Received: {metadata["received"]}')
      testRows.append([tOut[0], tOut[1].command, " ".join(result)])

    return printTemplate("runtime-description",
                         None,
                         styles=customStyles,
                         runtimeName=self._deployName,
                         deployable=status.deployable,
                         warningsList=status.warnings,
                         tipsList=status.tips,
                         errorsList=status.errors,
                         properties={
                             "headers": propHeaders,
                             "rows": propRows
                         },
                         tests={
                             "headers": testHeaders,
                             "rows": testRows
                         })

  def _decideAllPackages(self):
    rtPyProps, propError = self._getRuntimePythonProps()
    if propError is not None or rtPyProps is None:
      return
    missingModules = listMissingPackagesFromImports(rtPyProps.namespaceModules, None)
    missingPips = list(set([m[1] for m in missingModules]))
    mergedPackageList = mergePipPackageLists(self._pythonPackages or [], missingPips)
    mergedPackageList = addDependentPackages(mergedPackageList)
    mergedPackageList = scrubUnwantedPackages(mergedPackageList)
    mergedPackageList = annotateSpecialPackages(mergedPackageList)
    self.set_python_packages(mergedPackageList)
    self.set_system_packages(systemPackagesForPips(self._pythonPackages, self._systemPackages))

  def _getStatusNotes(self):
    tips: List[WarningErrorTip] = []
    warnings: List[WarningErrorTip] = []
    errors: List[WarningErrorTip] = []
    rtPyProps: Optional[RuntimePythonProps] = None

    # Errors
    if not self._deployName:
      errors.append(GenericError("This deployment needs a name."))
    rtPyProps, propError = self._getRuntimePythonProps()
    if propError is not None:
      errors.append(propError)
    for tOut in self._testOutputs:
      if tOut[0] == False:  # failed test
        errors.append(GenericError("This deployment has failing tests."))
        break
    if not self._api.isAuthenticated():
      errors.append(GenericError("You are not logged in to Modelbit. Please log in, then deploy."))

    # Warnings
    depPackages = self._pythonPackages
    if (rtPyProps is not None):
      warnings += getMissingPackageWarningsFromImportedModules(rtPyProps.namespaceModules, depPackages)
      # can re-enable once we also look in common files
      # warnings += getMissingLocalFileWarningsFromImportedModules(rtPyProps.namespaceModules, self._extraFiles)
      warnings += getProbablyNotAPackageWarnings(depPackages)
      if not self._dataframeMode:
        warnings += warningIfShouldBeUsingDataFrameWarning(rtPyProps.argNames, rtPyProps.argTypes)
      warnings += getVersionProbablyWrongWarnings(depPackages)
      if len(rtPyProps.functionsCallingGetModelButNoModels) > 0:
        warnings.append(getMissingModelDepsWarning(rtPyProps.functionsCallingGetModelButNoModels))
    warnings += getMissingPackageWarningsFromEnvironment(depPackages)

    localPyVersion = getInstalledPythonVersion()
    if self._pythonVersion != localPyVersion:
      warnings.append(DifferentPythonVerWarning(self._pythonVersion, localPyVersion))

    return RuntimeStatusNotes(tips, warnings, errors)

  def _getTests(self):
    if not callable(self._deployFunc) or self._deployFunc.__doc__ is None:
      return None
    funcName = self._deployFunc.__name__
    funcSource = self._sourceOverride if self._sourceOverride is not None else getFuncSource(self._deployFunc)
    if funcSource is None:
      return None
    tests = RuntimeApi(self._api).parseTests(funcName, funcSource)
    if tests:
      return tests
    return None

  def _runTest(self, test: DeploymentTestDesc):
    if not callable(self._deployFunc):
      return False
    if test.args == None:
      return self._deployFunc()
    return self._deployFunc(*test.args)  # type: ignore

  def _getTestOutputs(
      self, tests: List[DeploymentTestDesc]) -> List[Tuple[bool, DeploymentTestDesc, Dict[str, str]]]:
    return [self._getTestOutput(t) for t in tests]

  def _getTestOutput(self, test: DeploymentTestDesc) -> Tuple[bool, DeploymentTestDesc, Dict[str, str]]:

    if test.error:
      errorMessage = "Unable to run test."
      if test.error == DeploymentTestError.UnknownFormat.value:
        errorMessage = "Unknown test format"
      if test.error == DeploymentTestError.ExpectedNotJson.value:
        errorMessage = "Expected value must be JSON serializable"
      if test.error == DeploymentTestError.CannotParseArgs.value:
        errorMessage = "Unable to parse function arguments."
      return (False, test, {"error": errorMessage})

    result = self._runTest(test)
    try:
      jResult = json.loads(json.dumps(result))  # dump+load helps clean up numbers like 2.00000000001
      if jResult != test.expectedOutput:
        return (False, test, {"expected": json.dumps(test.expectedOutput), "received": json.dumps(jResult)})
    except:
      return (False, test, {"error": "Output must be JSON serializable.", "received": type(result).__name__})
    return (True, test, {"expected": json.dumps(test.expectedOutput)})

  def _collectDataFrameModeColumns(self, df: 'pandas.DataFrame') -> List[Dict[str, Union[str, Any]]]:
    if len(getFuncArgNames(self._deployFunc)) != 1:
      raise UserFacingError(
          "When using dataframe_mode, the deploy function can only have one input argument.")
    config: List[Dict[str, Any]] = []
    examples: Optional[Dict[str, Any]] = None
    if len(df) > 0:
      examples = cast(Dict[str, Any], json.loads(df.head(1).to_json(orient="records"))[0])  # type: ignore
    for col in cast(List[str], list(df.columns)):
      cf = {"name": col, "dtype": str(df[col].dtype)}
      if examples is not None:
        cf["example"] = examples[col]
      config.append(cf)
    return config


class Deployment(Runtime):

  def __init__(self,
               api: Optional[MbApi] = None,
               name: Optional[str] = None,
               deploy_function: Optional[Callable[..., Any]] = None,
               python_version: Optional[str] = None,
               requirements_txt_filepath: Optional[str] = None,
               requirements_txt_contents: Optional[List[str]] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               docker_run: Optional[str] = None,
               source_override: Optional[str] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               extra_files: Union[str, List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               job: Optional['m_jobs.ModelbitJobWrapper'] = None,
               require_gpu: bool = False):
    if api is None:
      api = mbApi()
    Runtime.__init__(self,
                     api=api,
                     name=name,
                     main_function=deploy_function,
                     python_version=python_version,
                     requirements_txt_filepath=requirements_txt_filepath,
                     requirements_txt_contents=requirements_txt_contents,
                     python_packages=python_packages,
                     system_packages=system_packages,
                     docker_run=docker_run,
                     source_override=source_override,
                     dataframe_mode=dataframe_mode,
                     example_dataframe=example_dataframe,
                     extra_files=extra_files,
                     skip_extra_files_dependencies=skip_extra_files_dependencies,
                     job=job,
                     require_gpu=require_gpu)

  def set_deploy_function(self, func: Callable[..., Any]):
    self._set_main_function(func)


def add_objects(api: MbApi, deployment: str, values: Dict[str, Any]):
  """add_object takes the name of a deployment and map of object names to objects.
  These objects will be pickled and stored in `data/object.pkl`
  and can be read using modelbit.load_value('data/object.pkl).
  """
  dataFiles: Dict[str, str] = {}
  for [name, val] in values.items():
    uploadResult = runtime_objects.describeAndUploadRuntimeObject(api, val, tryPickle(val, name), name)
    if uploadResult:
      dataFiles[f"data/{name}.pkl"] = uploadResult
  return _changeFilesAndDeploy(api, deployment, dataFiles)


def add_files(api: MbApi,
              deployment: str,
              files: Union[str, List[str], Dict[str, str]],
              modelbit_file_prefix: Optional[str] = None,
              strip_input_path: Optional[bool] = False):
  """ add_files takes the name of a deployment and either a list of files or
  a dict of local paths to deployment paths.
  modelbit_file_prefix is an optional folder prefix added to all files when uploaded. For example (deployment="score", files=['myModel.pkl'], modelbit_file_prefix="data")
  would upload myModel.pkl in the current directory to data/myModel.pkl in the deployment named score.
  """

  BranchApi(api).raiseIfProtected()

  dataFiles = runtime_objects.prepareFileList(api,
                                              files,
                                              modelbit_file_prefix=modelbit_file_prefix,
                                              strip_input_path=strip_input_path)
  if len(files) == 0:
    raise UserFacingError("At least one file is required, but the list of files is empty.")
  if len(json.dumps(dataFiles)) > 5_000_000:
    raise UserFacingError("Total file size exceeds maximum allowed (5MB). Use git or add fewer files.")
  return _changeFilesAndDeploy(api, deployment, dataFiles)


def _changeFilesAndDeploy(api: MbApi, deployment: str, dataFiles: Dict[str, str]):
  resp = RuntimeApi(api).updateRuntime(getCurrentBranch(), deployment, dataFiles)

  printTemplate(f"runtime-deployed",
                None,
                deploymentName=deployment,
                deployMessage=resp.message,
                deployTimeWords=_parseTimeFromDeployMessage(resp.message),
                runtimeOverviewUrl=resp.runtimeOverviewUrl)
  return None
