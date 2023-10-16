from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict
import inspect, re, string

from modelbit.api import MbApi
from modelbit.runtime import Deployment
from modelbit.utils import getFuncName, convertLambdaToDef

if TYPE_CHECKING:
  import pandas
  import modelbit.jobs as m_jobs


class SklearnPredictor:

  def __init__(self,
               skpredictor: Any,
               name: Optional[str] = None,
               python_version: Optional[str] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               extra_files: Union[List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               require_gpu: bool = False):
    self.skpredictor = skpredictor
    self.python_version = python_version
    self.python_packages = python_packages
    self.system_packages = system_packages
    self.dataframe_mode = dataframe_mode
    self.example_dataframe = example_dataframe
    self.extra_files = extra_files
    self.skip_extra_files_dependencies = skip_extra_files_dependencies
    self.require_gpu = require_gpu

    if name:
      self.name = name
    else:
      self.name = self.guessModelName()

  def guessModelName(self):
    try:
      codeContexts = [f.code_context for f in inspect.stack()]
      for ccList in codeContexts:
        if not ccList:
          continue
        for cc in ccList:
          captures = re.search(r"\.(deploy|train)\(([^\s,)]+)", cc)
          if captures:
            return captures.group(2)
    except Exception as _:
      pass
    return None

  def guessNumArgs(self):
    for i in range(1, 25):
      try:
        args = [j for j in range(i)]
        self.skpredictor.predict([args])
        return i
      except Exception:
        pass
    return None

  def makeDeployment(self, api: MbApi):
    skpredictor = self.skpredictor

    varName = "skpredictor"
    if self.name:
      varName = self.name
    globals()[varName] = skpredictor  # put the same value to globals so it acts more like a notebook cell

    guessedArgCount = self.guessNumArgs()
    if guessedArgCount:
      letters = list(string.ascii_lowercase)
      argNames = letters[0:guessedArgCount]
      argsWithTypes = ", ".join([f"{ltr}: float" for ltr in argNames])
      funcSource = "\n".join([
          f"def predict({argsWithTypes}) -> float:",
          f"  return {varName}.predict([[{', '.join(argNames)}]])[0]", f""
      ])
    else:
      funcSource = "\n".join([f"def predict(*args: Any):", f"  return {varName}.predict([args])[0]", f""])

    exec(funcSource)
    deploy_function = locals()["predict"]

    return Deployment(api=api,
                      deploy_function=deploy_function,
                      source_override=funcSource,
                      python_version=self.python_version,
                      python_packages=self.python_packages,
                      system_packages=self.system_packages,
                      name=self.name,
                      dataframe_mode=self.dataframe_mode,
                      example_dataframe=self.example_dataframe,
                      extra_files=self.extra_files,
                      skip_extra_files_dependencies=self.skip_extra_files_dependencies,
                      require_gpu=self.require_gpu)


class LambdaWrapper:

  def __init__(self,
               lambdaFunc: Any,
               name: Optional[str] = None,
               python_version: Optional[str] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               extra_files: Union[List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               require_gpu: bool = False):

    self.lambdaFunc = lambdaFunc
    self.python_version = python_version
    self.python_packages = python_packages
    self.system_packages = system_packages
    self.dataframe_mode = dataframe_mode
    self.example_dataframe = example_dataframe
    self.extra_files = extra_files
    self.skip_extra_files_dependencies = skip_extra_files_dependencies
    self.require_gpu = require_gpu
    self.name = name if name is not None else getFuncName(self.lambdaFunc, "predict")

  def makeDeployment(self, api: MbApi):
    deployFunction, funcSource = convertLambdaToDef(self.lambdaFunc, self.name)

    return Deployment(api=api,
                      deploy_function=deployFunction,
                      source_override=funcSource,
                      python_version=self.python_version,
                      python_packages=self.python_packages,
                      system_packages=self.system_packages,
                      name=self.name,
                      dataframe_mode=self.dataframe_mode,
                      example_dataframe=self.example_dataframe,
                      extra_files=self.extra_files,
                      skip_extra_files_dependencies=self.skip_extra_files_dependencies,
                      require_gpu=self.require_gpu)


class RuntimeJobWrapper:

  def __init__(
      self,
      job: 'm_jobs.ModelbitJobWrapper',
      name: str,
      python_version: Optional[str] = None,
      python_packages: Optional[List[str]] = None,
      system_packages: Optional[List[str]] = None,
      extra_files: Union[str, List[str], Dict[str, str], None] = None,
      skip_extra_files_dependencies: bool = False,
  ):
    self.job = job
    self.python_version = python_version
    self.python_packages = python_packages
    self.system_packages = system_packages
    self.extra_files = extra_files
    self.skip_extra_files_dependencies = skip_extra_files_dependencies
    self.name = name

  def makeDeployment(self, api: MbApi):
    return Deployment(api=api,
                      deploy_function=None,
                      job=self.job,
                      python_version=self.python_version,
                      python_packages=self.python_packages,
                      system_packages=self.system_packages,
                      name=self.name,
                      extra_files=self.extra_files,
                      skip_extra_files_dependencies=self.skip_extra_files_dependencies)
