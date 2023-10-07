from typing import Any, Dict, List
from modelbit.api.api import MbApi
from modelbit.helpers import getCurrentBranch
from modelbit.internal.secure_storage import DownloadableObjectInfo


class RegistryApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def delete(self, names: List[str]):
    self.api.getJsonOrThrow("api/cli/v1/registry/delete", {"branch": getCurrentBranch(), "names": names})

  def storeContentHashAndMetadata(self, objects: Dict[str, Dict[str, Any]]):
    self.api.getJsonOrThrow("api/cli/v1/registry/set", {"branch": getCurrentBranch(), "objects": objects})

  def getRegistryDownloadInfo(self):
    resp = self.api.getJsonOrThrow("api/cli/v1/registry/get_signed_url", {"branch": getCurrentBranch()})
    if "downloadInfo" in resp:
      return RegistryDownloadInfo(resp["downloadInfo"])


class RegistryDownloadInfo(DownloadableObjectInfo):

  def __init__(self, data: Dict[str, Any]):
    super().__init__(data)
    self.id: str = data["id"]

  def cachekey(self) -> str:
    return self.id
