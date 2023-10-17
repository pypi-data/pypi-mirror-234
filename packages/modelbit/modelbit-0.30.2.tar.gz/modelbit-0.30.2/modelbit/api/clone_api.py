from typing import Optional, Any, Dict

from modelbit.api import MbApi
from modelbit.internal.local_config import saveWorkspaceConfig
from modelbit.cli.ui import output
from time import sleep
import logging
import os

logger = logging.getLogger(__name__)


class CloneInfo:

  def __init__(self, data: Dict[str, Any]):
    self.workspaceId: str = data["workspaceId"]
    self.cluster: str = data["cluster"]
    self.gitUserAuthToken: str = data["gitUserAuthToken"]
    self.mbRepoUrl: str = data["mbRepoUrl"]
    self.forgeRepoUrl: Optional[str] = data.get("forgeRepoUrl", None)
    self.numSshKeys: int = data.get("numSshKeys", -1)

  def __str__(self) -> str:
    return str(vars(self))


class CloneApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def getCloneInfo(self) -> Optional[CloneInfo]:
    resp = self.api.getJson("api/cli/v1/clone_info")
    if "errorCode" in resp:
      logger.info(f"Got response {resp}")
      return None
    if _isClusterRedirectResponse(resp):
      self.api.setUrls(resp["cluster"])
      return None
    return CloneInfo(resp)


def _isClusterRedirectResponse(resp: Dict[str, Any]) -> bool:
  return "cluster" in resp and not "workspaceId" in resp
