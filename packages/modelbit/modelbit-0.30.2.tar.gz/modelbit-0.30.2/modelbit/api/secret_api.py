import base64
import logging
from typing import Any, Dict, Optional

from .api import MbApi

logger = logging.getLogger(__name__)


class SecretDesc:
  secretValue: Optional[bytes] = None

  def __init__(self, data: Dict[str, Any]):
    if "secretValue64" in data:
      self.secretValue = base64.b64decode(data["secretValue64"])

  def __repr__(self):
    return str(self.__dict__)


class SecretApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def getSecret(self, branch: str, secretName: str, runtimeName: str) -> Optional[SecretDesc]:
    resp = self.api.getJsonOrThrow("api/cli/v1/secrets/get",
                                   dict(secretName=secretName, runtimeName=runtimeName, branch=branch))
    return SecretDesc(resp['secretInfo']) if resp is not None else None
