import logging
import os

from modelbit.api import MbApi
from modelbit.internal.cache import stubCacheFilePath
from modelbit.internal.describe import shouldUploadFile
from modelbit.internal.file_stubs import fromYaml
from modelbit.internal.runtime_objects import describeAndUploadRuntimeObject, downloadRuntimeObject
from modelbit.internal.secure_storage import calcHash

logger = logging.getLogger(__name__)


class GitFilter:

  def __init__(self, workspaceId: str, mbApi: MbApi):
    self.workspaceId = workspaceId
    self.api = mbApi

  def clean(self, filepath: str, content: bytes, skipCache=False) -> bytes:
    if not shouldUploadFile(filepath, content):
      logger.info(f"Ignoring {filepath}")
      if content:
        return content
      return b''
    contentHash = calcHash(content)
    logger.info(f"Cleaning {filepath} hash={contentHash}")
    cacheFilepath = None
    if not skipCache:
      cacheFilepath = stubCacheFilePath(self.workspaceId, contentHash)
      if os.path.exists(cacheFilepath):  # Try cache
        try:
          with open(cacheFilepath, "rb") as f:
            yamlContent = f.read()
            if fromYaml(yamlContent) == contentHash:
              return yamlContent
        except Exception as e:
          logger.info("Failed to read from cache", exc_info=e)

    yamlContent = describeAndUploadRuntimeObject(self.api, None, content, filepath).encode('utf-8')
    if not skipCache and cacheFilepath is not None:
      with open(cacheFilepath, "wb") as f:
        f.write(yamlContent)
    return yamlContent

  def smudge(self, filepath: str, content: bytes) -> bytes:
    if os.getenv("SKIP_SMUDGE") == "true":
      return content
    try:
      contentHash = fromYaml(content)
    except Exception:
      logger.info(f"Not smudging {filepath}")
      return content
    if contentHash is None:
      return content
    # Store in cache
    # Otherwise diffs trigger if the locally environment differs
    cacheFilepath = stubCacheFilePath(self.workspaceId, contentHash)
    with open(cacheFilepath, "wb") as f:
      f.write(content)

    logger.info(f"Smudging {filepath} hash={contentHash}")
    data = downloadRuntimeObject(self.api, contentHash, filepath)
    return data
