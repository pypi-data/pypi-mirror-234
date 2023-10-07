import logging
from datetime import datetime
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)
LARGE_FILE_STUB_SENTINEL = b'_: MBFileStub'
SCHEMA_VERSION = 1


def repr_str(dumper: yaml.Dumper, data: str):
  if '\n' in data:
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def toYaml(contentHash: str, fileSize: int, objDesc: Dict[str, Any]) -> str:
  metadata: Dict[str, Any] = dict(fileSize=fileSize, **objDesc)

  obj = _toFileStubDict(contentHash, metadata)
  yaml.add_representer(str, repr_str)
  return yaml.dump(obj, width=1000)


def fromYaml(content: bytes) -> Optional[str]:
  if not content.startswith(LARGE_FILE_STUB_SENTINEL):
    return None

  obj = yaml.safe_load(content.decode("utf-8"))
  if type(obj) is dict and "contentHash" in obj:
    return obj["contentHash"]
  return None


def _toFileStubDict(contentHash: str, objDesc: Dict[str, Any]) -> Dict[str, Any]:
  return {
      "_": "MBFileStub",
      "createdAt": datetime.utcnow().replace(microsecond=0),
      "contentHash": contentHash,
      "metadata": objDesc,
      "schemaVersion": SCHEMA_VERSION
  }
