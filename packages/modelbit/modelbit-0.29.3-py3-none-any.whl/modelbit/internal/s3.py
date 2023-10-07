#!/usr/bin/env python3
import base64
import os
from typing import cast

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from modelbit.utils import boto3Client


def getS3FileBytes(keySuffix: str):
  import zstandard  # type: ignore
  decData = downloadDecryptS3File(keySuffix)
  if decData is not None:
    return cast(bytes, zstandard.decompress(decData))  # type: ignore
  return None


def downloadDecryptS3File(dsKey: str):
  _workspaceId = os.getenv('WORKSPACE_ID')
  _pystateBucket = os.getenv('PYSTATE_BUCKET')
  _pystateKeys = os.getenv('PYSTATE_KEYS')
  if _workspaceId == None or _pystateBucket == None or _pystateKeys == None:
    raise Exception(f"EnvVar Missing: WORKSPACE_ID, PYSTATE_BUCKET, PYSTATE_KEYS")
  try:
    dsKey = f'{_workspaceId}/{dsKey}'
    s3Obj = boto3Client('s3').get_object(Bucket=_pystateBucket, Key=dsKey)  # type: ignore
    fileKeyEnc = base64.b64decode(s3Obj['Metadata']["x-amz-key"])  # type: ignore
    fileIv = base64.b64decode(s3Obj['Metadata']["x-amz-iv"])  # type: ignore
    for key64 in str(_pystateKeys).split(","):
      cipher = AES.new(base64.b64decode(key64), AES.MODE_ECB)  # type: ignore
      fileKey = unpad(cipher.decrypt(fileKeyEnc), AES.block_size)
      cipher = AES.new(fileKey, AES.MODE_CBC, fileIv)  # type: ignore
      bodyDataEnc = cast(bytes, s3Obj['Body'].read())  # type: ignore
      decState = unpad(cipher.decrypt(bodyDataEnc), AES.block_size)
      return decState
  except Exception as err:
    strErr = str(err)
    if 'AccessDenied' not in strErr and 'NoSuchKey' not in strErr:
      raise err
  return None
