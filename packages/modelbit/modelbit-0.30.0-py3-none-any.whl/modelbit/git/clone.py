import logging
import os
import subprocess
import sys
from typing import Optional, Tuple

from modelbit.api import CloneApi, CloneInfo
from modelbit.cli.ui import chooseOption, output
from modelbit.internal.auth import mbApi
from modelbit.internal.local_config import saveWorkspaceConfig

logger = logging.getLogger(__name__)


def pickGitOrigin(cloneInfo: CloneInfo, origin: Optional[str]) -> Tuple[str, bool]:
  # Origin can be passed in via cmdline. If modelbit, use internal, otherwise use external
  if origin == "modelbit":
    return (cloneInfo.mbRepoUrl, True)
  elif origin is not None:
    if cloneInfo.forgeRepoUrl is None:
      output("Forced external origin but no external repository is configured.")
      exit(1)
    return (cloneInfo.forgeRepoUrl, False)

  if cloneInfo.forgeRepoUrl is None:
    return (cloneInfo.mbRepoUrl, True)

  forgeHost = cloneInfo.forgeRepoUrl.split(":")[0]
  forgeHost = forgeHost.split("@")[1] if forgeHost.index("@") else forgeHost

  action = chooseOption("Choose a remote",
                        [f"Modelbit: {cloneInfo.mbRepoUrl}", f"{forgeHost}: {cloneInfo.forgeRepoUrl}"], 0)
  if action is None:
    output("Nothing chosen")
    exit(1)
  if action.startswith("Modelbit"):
    return (cloneInfo.mbRepoUrl, True)
  return cloneInfo.forgeRepoUrl, False


def doGitClone(workspaceId: str, apiHost: str, gitUrl: str, targetDir: str) -> None:
  cloneConfig = [
      "--config", f"modelbit.restendpoint={apiHost}api/format", "--config",
      "filter.modelbit.process=modelbit gitfilter process", "--config", "filter.modelbit.required",
      "--config", "merge.renormalize=true"
  ]

  env = dict(os.environ.items())
  env["MB_WORKSPACE_ID"] = workspaceId
  logger.info(f"Cloning {gitUrl} into {targetDir} for {workspaceId}")
  try:
    subprocess.run(["git", "clone", *cloneConfig, gitUrl, targetDir],
                   stdin=sys.stdin,
                   stdout=sys.stdout,
                   stderr=sys.stderr,
                   check=True,
                   env=env)
  except subprocess.CalledProcessError:
    output(
        "There was an error cloning your repository. Some large files may not have been restored. Please contact support."
    )


def clone(targetDir: str = "modelbit", origin: Optional[str] = None) -> None:
  if targetDir and os.path.exists(targetDir):
    output(f"Error: Unable to clone repository. The target directory '{targetDir}' already exists.")
    exit(1)

  api = mbApi(source="clone")
  cloneInfo = CloneApi(api).getCloneInfo()
  if cloneInfo is None:
    raise Exception("Failed to authenticate. Please try again.")
  saveWorkspaceConfig(cloneInfo.workspaceId, cloneInfo.cluster, cloneInfo.gitUserAuthToken)

  gitUrl, _ = pickGitOrigin(cloneInfo, origin)
  if gitUrl == cloneInfo.mbRepoUrl and cloneInfo.numSshKeys == 0:
    errMsg = "Error: You must upload an SSH key to clone from Modelbit. See https://doc.modelbit.com/git/getting-started-with-git"
    output(errMsg)
    exit(1)
  doGitClone(cloneInfo.workspaceId, api.getApiHost(), gitUrl, targetDir)
