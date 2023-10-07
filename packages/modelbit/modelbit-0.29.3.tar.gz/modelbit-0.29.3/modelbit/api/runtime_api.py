import logging
from typing import Any, Dict, List, Optional, Union

from .api import MbApi
from .common import OwnerInfo

logger = logging.getLogger(__name__)


class RuntimeDesc:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.name: str = data["name"]
    self.version: str = data["version"]
    self.deployedAtMs: int = data["deployedAtMs"]
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class DeployedRuntimeDesc:

  def __init__(self, data: Dict[str, Any]):
    self.name: str = data["name"]
    self.version: Optional[str] = data.get("version", None)
    self.branch: str = data["branch"]
    self.runtimeOverviewUrl: str = data["runtimeOverviewUrl"]
    self.message: str = data["message"]


class DeploymentTestDesc:

  def __init__(self, data: Dict[str, Any]):
    self.command: str = data.get("command", "")
    self.expectedOutput: Union[str, Dict[Union[str, int, float, bool], Any]] = data.get("expectedOutput", "")
    self.args: Optional[List[Any]] = data.get("args", None)
    self.error: Optional[str] = data.get("error", None)


class RuntimeApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def listDeployments(self, branch: str) -> List[RuntimeDesc]:
    resp = self.api.getJsonOrThrow("api/cli/v1/runtimes/list", {"branch": branch})
    deployments = [RuntimeDesc(ds) for ds in resp.get("runtimes", [])]
    return deployments

  def createRuntime(self, branch: str, createRuntimeRequest: Dict[str, Any]) -> DeployedRuntimeDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/runtimes/create", {
        "branch": branch,
        "createRuntimeRequest": createRuntimeRequest
    })
    return DeployedRuntimeDesc(resp["runtime"])

  def updateRuntime(self, branch: str, runtimeName: str, dataFiles: Dict[str, str]) -> DeployedRuntimeDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/runtimes/update", {
        "branch": branch,
        "runtimeName": runtimeName,
        "dataFiles": dataFiles,
    })
    return DeployedRuntimeDesc(resp["runtime"])

  def parseTests(self, funcName: str, funcSource: str) -> List[DeploymentTestDesc]:
    resp = self.api.getJsonOrThrow("api/cli/v1/runtimes/parse_tests", {
        "funcName": funcName,
        "funcSource": funcSource,
    })
    return [DeploymentTestDesc(d) for d in resp["tests"]] if resp["tests"] is not None else []
