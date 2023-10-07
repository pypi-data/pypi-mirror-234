import logging
import os
from threading import Thread
from time import sleep
from typing import Optional

from modelbit.api import MbApi
from modelbit.error import UserFacingError
from modelbit.helpers import getCurrentBranch, pkgVersion, setCurrentBranch
from modelbit.utils import inDeployment, inModelbitCI, inNotebook
from modelbit.ux import COLORS, makeCssStyle, printTemplate

logger = logging.getLogger(__name__)

__mbApi: MbApi = MbApi()


def mbApi(region: Optional[str] = None,
          source: Optional[str] = None,
          refreshAuth: bool = True,
          branch: Optional[str] = None) -> MbApi:
  global __mbApi
  if not isAuthenticated():
    _performLogin(__mbApi, refreshAuth=refreshAuth, region=region, source=source, branch=branch)
  elif branch is not None:
    setCurrentBranch(branch)
    _printAuthenticatedMessage(__mbApi)
  return __mbApi


def mbApiReadOnly() -> MbApi:
  global __mbApi
  return __mbApi


def isAuthenticated() -> bool:
  if inDeployment():
    return True
  return mbApiReadOnly().isAuthenticated()


def apiKeyFromEnv() -> Optional[str]:
  return os.getenv("MB_API_KEY")


def workspaceNameFromEnv() -> Optional[str]:
  return os.getenv("MB_WORKSPACE_NAME")


###


def _performLogin(api: MbApi,
                  refreshAuth: bool = False,
                  region: Optional[str] = None,
                  source: Optional[str] = None,
                  branch: Optional[str] = None):
  setCurrentBranch(branch or _determineCurrentBranch())
  if inDeployment() or (api.isAuthenticated() and not refreshAuth):
    return
  elif apiKeyFromEnv() is not None:
    _performApiKeyLogin(api, region)
  elif inNotebook() or inModelbitCI():
    _performBrowserLogin(api, refreshAuth, region, source=source)
  else:
    if not _performCLILogin(api):
      _performBrowserLogin(api, refreshAuth, region, waitForResponse=True, source=source)


def _performCLILogin(api: MbApi):
  from modelbit.git.workspace import findWorkspace
  from modelbit.internal.local_config import getWorkspaceConfig
  try:
    config = getWorkspaceConfig(findWorkspace())
    if not config:
      raise KeyError("Workspace credentials not found")
  except KeyError:
    return False
  api.setUrls(config.cluster)
  api.setToken(config.gitUserAuthToken.replace("mbpat-", ""))
  if not api.refreshAuthentication(getCurrentBranch()):
    return False
  _printAuthenticatedMessage(api)
  return True


def _performApiKeyLogin(api: MbApi, region: Optional[str]):
  apiKey = apiKeyFromEnv()
  workspaceName = workspaceNameFromEnv()
  if apiKey is None:
    return
  if ":" not in apiKey:
    raise UserFacingError("Incorrect API Key. Please check MB_API_KEY.")
  if workspaceName is None:
    raise UserFacingError("Missing env var MB_WORKSPACE_NAME.")

  apiKeyId = apiKey.split(':')[0]
  logger.info(
      f"Attempting to log in with API Key {apiKeyId} to workspace {workspaceName} branch {getCurrentBranch()}."
  )
  if region is not None:
    api.setUrls(f"{region}.modelbit.com")
  source = "notebook" if inNotebook() else "terminal"
  nbEnv = api.loginWithApiKey(apiKey, workspaceName, source)
  if nbEnv is None:
    raise UserFacingError(f"Failed to log in with API Key {apiKeyId} to workspace {workspaceName}.")
  _printAuthenticatedMessage(api)


def _performBrowserLogin(api: MbApi,
                         refreshAuth: bool = False,
                         region: Optional[str] = None,
                         waitForResponse: bool = False,
                         source: Optional[str] = None):
  if region is not None:
    api.setUrls(f"{region}.modelbit.com")
  if (refreshAuth):
    api.refreshAuthentication(getCurrentBranch())
  displayId = "mbLogin"
  _printLoginMessage(api, source, displayId)

  def _pollForLoggedIn():
    triesLeft = 150
    while not api.isAuthenticated() and triesLeft > 0:
      triesLeft -= 1
      sleep(3)
      api.refreshAuthentication(getCurrentBranch())
    if api.isAuthenticated():
      _printAuthenticatedMessage(api, displayId)
    else:
      printTemplate("login-timeout", displayId)

  if waitForResponse:
    _pollForLoggedIn()
  else:
    loginThread = Thread(target=_pollForLoggedIn)
    if not inModelbitCI():
      loginThread.start()


def _determineCurrentBranch():
  from modelbit.git.workspace import findCurrentBranch
  return os.getenv("BRANCH", None) or findCurrentBranch() or "main"


def _printAuthenticatedMessage(api: MbApi, displayId: Optional[str] = None):
  inRegion: Optional[str] = None
  if api.getCluster() != api._DEFAULT_CLUSTER:
    inRegion = api._region
  loginState = api.loginState
  if loginState is None:
    return
  styles = {
      "connected": makeCssStyle({
          "color": COLORS["success"],
          "font-weight": "bold",
      }),
      "info": makeCssStyle({
          "font-family": "monospace",
          "font-weight": "bold",
          "color": COLORS["brand"],
      })
  }
  printTemplate("authenticated",
                displayId,
                updateDisplayId=True,
                styles=styles,
                email=loginState.userEmail,
                workspace=loginState.workspaceName,
                inRegion=inRegion,
                currentBranch=getCurrentBranch(),
                needsUpgrade=_pipUpgradeInfo(loginState.mostRecentVersion),
                warningsList=[])


def _printLoginMessage(api: MbApi, source: Optional[str] = None, displayId: Optional[str] = None):
  if source is None:
    source = "notebook" if inNotebook() else "terminal"
  linkUrl = api.getLoginLink(source, getCurrentBranch())
  displayUrl = f'modelbit.com/t/{(api.authToken or "")[0:10]}...'
  printTemplate("login",
                displayId,
                displayUrl=displayUrl,
                linkUrl=linkUrl,
                source=source,
                needsUpgrade=_pipUpgradeInfo(api.loginState and api.loginState.mostRecentVersion or None))


def _pipUpgradeInfo(mostRecentVersion: Optional[str]):
  if inDeployment():
    return None  # runtime environments don't get upgraded
  latestVer = mostRecentVersion

  def ver2ints(ver: str):
    return [int(v) for v in ver.split(".")]

  nbVer = pkgVersion
  if latestVer and ver2ints(latestVer) > ver2ints(nbVer):
    return {"installed": nbVer, "latest": latestVer}
  return None
