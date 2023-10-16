import base64
import logging
import os
import sys
from io import BytesIO, StringIO, BufferedReader
from typing import Any, Dict, TextIO, Union, List, cast
import tempfile
import boto3
import requests

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from modelbit.internal.cache import objectCacheFilePath
from modelbit.utils import inNotebook
from tqdm import tqdm
from abc import ABCMeta, abstractmethod
from modelbit.internal.describe import calcHash

logger = logging.getLogger(__name__)

defaultRequestTimeout = 10
readBlockSize = AES.block_size * 1024 * 1024  # 16MB


class UploadableObjectInfo:

  def __init__(self, data: Dict[str, Any]):
    self.bucket: str = data["bucket"]
    self.s3Key: str = data["s3Key"]
    self.awsCreds: Dict[str, str] = data["awsCreds"]
    self.metadata: Dict[str, str] = data["metadata"]
    self.fileKey64: str = data["fileKey64"]
    self.fileIv64: str = data["fileIv64"]
    self.objectExists: bool = data["objectExists"]


class DownloadableObjectInfo(metaclass=ABCMeta):

  def __init__(self, data: Dict[str, Any]):
    self.workspaceId: str = data["workspaceId"]
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]

  @abstractmethod
  def cachekey(self) -> str:
    raise Exception("NYI")


def putSecureData(uploadInfo: UploadableObjectInfo, obj: bytes, desc: str) -> None:
  if uploadInfo.objectExists:
    return
  import zstandard
  cipher = AES.new(  # type: ignore
      mode=AES.MODE_CBC,
      key=base64.b64decode(uploadInfo.fileKey64),
      iv=base64.b64decode(uploadInfo.fileIv64))

  chunkSize = 2**15
  objReader = BytesIO(obj)
  with tempfile.NamedTemporaryFile() as tf:
    cCtx = zstandard.ZstdCompressor()
    chunker = cCtx.chunker(chunk_size=chunkSize, size=len(obj))
    while True:
      inChunk = objReader.read(chunkSize)
      if not inChunk:
        break
      for outChunk in cast(List[bytes], chunker.compress(inChunk)):  # type: ignore
        tf.write(cipher.encrypt(outChunk))

    finalChunks = cast(List[bytes], list(chunker.finish()))  # type: ignore
    finalChunk = b"".join(finalChunks)
    tf.write(cipher.encrypt(pad(finalChunk, AES.block_size)))
    length = tf.tell()
    tf.seek(0)
    with open(tf.name, "rb") as inFile:
      _uploadFile(uploadInfo, inFile, length, desc)


def getSecureData(dri: DownloadableObjectInfo, desc: str) -> Union[bytes, memoryview]:
  if not dri:
    raise Exception("Download info missing from API response.")
  filepath = objectCacheFilePath(dri.workspaceId, dri.cachekey())

  if os.path.exists(filepath):  # Try cache
    try:
      return _decryptAndValidate(filepath, dri)
    except Exception as e:
      logger.info("Failed to read from cache", exc_info=e)

  _downloadFile(dri, filepath, desc)
  return _decryptAndValidate(filepath, dri)


def _uploadFile(uploadInfo: UploadableObjectInfo, body: BufferedReader, bodySize: int, desc: str) -> None:
  s3Client = boto3.client('s3', **uploadInfo.awsCreds)  # type: ignore
  outputStream: TextIO = sys.stdout
  if not inNotebook():  # printing to stdout breaks git's add file flow
    outputStream = sys.stderr
  if os.getenv('MB_TXT_MODE'):
    outputStream = StringIO()
  with body as b, tqdm(total=bodySize,
                       unit='B',
                       unit_scale=True,
                       miniters=1,
                       desc=f"Uploading '{desc}'",
                       file=outputStream) as t:
    s3Client.upload_fileobj(  # type: ignore
        b,
        uploadInfo.bucket,
        uploadInfo.s3Key,
        ExtraArgs={"Metadata": uploadInfo.metadata},
        Callback=lambda bytes_transferred: t.update(bytes_transferred))  # type: ignore


def _downloadFile(dri: DownloadableObjectInfo, filepath: str, desc: str) -> None:
  logger.info(f"Downloading to {filepath}")
  outputStream: TextIO = sys.stdout
  if not inNotebook():  # printing to stdout breaks git's add file flow
    outputStream = sys.stderr
  if os.getenv('MB_TXT_MODE'):
    outputStream = StringIO()
  resp = requests.get(dri.signedDataUrl, stream=True, timeout=defaultRequestTimeout)
  total = int(resp.headers.get('content-length', 0))
  with open(filepath, "wb") as f, tqdm(total=total,
                                       unit='B',
                                       unit_scale=True,
                                       miniters=1,
                                       desc=f"Downloading '{desc}'",
                                       file=outputStream) as t:
    for data in resp.iter_content(chunk_size=32 * 1024):
      size = f.write(data)
      t.update(size)


ZSTD_MAGIC_NUMBER = b"\x28\xB5\x2F\xFD"
GZIP_MAGIC_NUMBER = b"\x1f\x8b"


def _isLikelyZstd(data: bytes) -> bool:
  return data[0:4] == ZSTD_MAGIC_NUMBER


def _isLikelyGzip(data: bytes) -> bool:
  return data[0:2] == GZIP_MAGIC_NUMBER


# Cipher is stateful, so we need to make new ones for each read operation
def _makeCipher(dri: DownloadableObjectInfo) -> Any:
  return AES.new(base64.b64decode(dri.key64), AES.MODE_CBC, iv=base64.b64decode(dri.iv64))  # type: ignore


def _decryptZstd(cipher: Any, data: BufferedReader) -> memoryview:
  import zstandard
  bytesStream = BytesIO()
  dCtx = zstandard.ZstdDecompressor()
  dCom = dCtx.stream_writer(bytesStream)
  while True:
    rData = data.read(readBlockSize)
    if not rData:
      break
    chunk = cipher.decrypt(rData)
    if len(chunk) != readBlockSize or len(data.peek(1)) == 0:  # last block
      chunk = unpad(chunk, AES.block_size)
    dCom.write(chunk)
  return bytesStream.getbuffer()


def _decryptAndValidate(filepath: str, dri: DownloadableObjectInfo) -> Union[bytes, memoryview]:
  with open(filepath, "rb") as f:
    head = _makeCipher(dri).decrypt(f.read(AES.block_size))

  uncompressedData: Union[bytes, memoryview] = b''  # helps mypy with type checking
  with open(filepath, "rb") as data:
    if _isLikelyZstd(head):
      uncompressedData = _decryptZstd(_makeCipher(dri), data)
    elif _isLikelyGzip(head):
      import zlib
      zData = unpad(_makeCipher(dri).decrypt(data.read()), AES.block_size)
      uncompressedData = zlib.decompress(zData, zlib.MAX_WBITS | 32)
    else:
      raise Exception("Unknown compression format")

  actualHash = calcHash(uncompressedData)
  if hasattr(dri, "contentHash"):
    if actualHash != dri.contentHash:  #type: ignore
      raise ValueError(
          f"Hash mismatch. Tried to fetch {dri.contentHash}, calculated {actualHash}")  #type: ignore
  return uncompressedData
