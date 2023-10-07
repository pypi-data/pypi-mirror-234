import logging
import sys
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait

from typing import BinaryIO, Callable, List, NoReturn, Optional, Tuple, Iterator, Dict, Set

logger = logging.getLogger(__name__)
FLUSH_PACKET = b"0000"


def passThrough(pathname, content: bytes) -> bytes:
  return content


def toPkts(s: bytes) -> Iterator[bytes]:
  size = len(s)
  offset = 0
  limit = min(size, 65516)
  while offset < size:
    yield b"%04x%s" % (limit + 4, s[offset:offset + limit])
    offset += limit
    limit = min(size - offset, 65516)


GIT_FILTER_THREADS = 10
MAX_FILE_DOWNLOAD_WAIT_SEC = 3600


class GitProtocolBase:
  """ Implements git-protocol. To aid debugging export GIT_TRACE_PACKET=1
      Roughly, a packet-based protocol. Each packet starts with 4 hex digits specifying
      the length.
      https://github.com/git/git/blob/master/Documentation/gitprotocol-common.txt
  """

  def __init__(self, inStream: Optional[BinaryIO] = None, outStream: Optional[BinaryIO] = None):
    self.inStream = inStream or sys.stdin.buffer
    self.outStream = outStream or sys.stdout.buffer

  def write(self, b) -> None:
    if b is FLUSH_PACKET:
      self.outStream.write(b)
    else:
      for pkt in toPkts(b):
        self.outStream.write(pkt)
    self.outStream.flush()

  def readKVData(self) -> List[Tuple[str, str]]:
    data = []
    while True:
      sizeHex = self.inStream.read(4)
      if len(sizeHex) == 0:
        raise EOFError
      size = int(sizeHex, 16)
      if size == 0:
        break
      pkt = self.inStream.read(size - 4)
      if b"=" in pkt:
        (k, v) = parseKv(pkt)
        data.append((k, v))
    return data

  def readBinaryData(self) -> bytes:
    data: List[bytes] = []
    while True:
      size = int(self.inStream.read(4), 16)
      if size == 0:
        break
      data.append(self.inStream.read(size - 4))
    return b"".join(data)


class GitProtocol(GitProtocolBase):

  def __init__(self,
               smudge: Optional[Callable[[str, bytes], bytes]] = None,
               clean: Optional[Callable[[str, bytes], bytes]] = None):
    super().__init__()
    self.smudge = smudge if smudge is not None else passThrough
    self.clean = clean if clean is not None else passThrough
    self.executor = ThreadPoolExecutor(max_workers=GIT_FILTER_THREADS)
    self.smudgeFutures: Set[Future] = set()
    self.smudgesAwaitingPickup: Dict[str, bytes] = dict()

  def versionHandshake(self) -> None:
    [version] = self.readKVData()
    # TODO: Process handshake
    self.write(b"git-filter-server\n")
    self.write(b"version=2\n")
    self.write(FLUSH_PACKET)

  def capabilitiesHandshake(self) -> None:
    caps = self.readKVData()
    # TODO: Process capabilities
    self.write(b"capability=clean\n")
    self.write(b"capability=smudge\n")
    self.write(b"capability=delay\n")
    self.write(FLUSH_PACKET)

  def readCommand(self) -> Tuple[str, str, bytes, bool]:
    hdr = dict(self.readKVData())
    command = hdr["command"].strip()
    pathname = hdr.get("pathname", "").strip()
    candelay = hdr.get("can-delay", "0").strip() == "1"
    content = self.readBinaryData() if command in ["smudge", "clean"] else b''
    return (command, pathname, content, candelay)

  def writeSuccess(self, content: Optional[bytes]) -> None:
    self.write(b"status=success\n")
    self.write(FLUSH_PACKET)
    if content and len(content):
      self.write(content)
      if type(content) is memoryview:
        content.release()  # free this copy of the data since we've handed it off to git
    self.write(FLUSH_PACKET)
    self.write(FLUSH_PACKET)

  def writeError(self) -> None:
    self.write(b"status=error\n")
    self.write(FLUSH_PACKET)

  def writeDelayed(self) -> None:
    self.write(b"status=delayed\n")
    self.write(FLUSH_PACKET)

  def scheduleSmudge(self, pathname, content) -> None:
    self.smudgeFutures.add(
        self.executor.submit(lambda pathname, content: [pathname, self.smudge(pathname, content)], pathname,
                             content))

  def _waitForAnyFuture(self) -> None:
    logger.info("Waiting futures=%d", len(self.smudgeFutures))
    done, not_done = wait(self.smudgeFutures, timeout=MAX_FILE_DOWNLOAD_WAIT_SEC, return_when=FIRST_COMPLETED)
    if len(done) == 0 and len(not_done) > 0:
      raise Exception("Failed to wait for file downloads")
    for future in done:
      pathname, content = future.result()
      self.smudgesAwaitingPickup[pathname] = content
    self.smudgeFutures = not_done

  def writeListOfAvailableBlobs(self) -> None:
    # If there are no available blobs, wait for some to come in
    if (len(self.smudgesAwaitingPickup) == 0):
      self._waitForAnyFuture()

    logger.info("availableBlobs=%d futures=%d", len(self.smudgesAwaitingPickup), len(self.smudgeFutures))
    for pathname in self.smudgesAwaitingPickup.keys():
      self.write(b"pathname=%s\n" % bytes(pathname, "utf8"))
    self.write(FLUSH_PACKET)
    self.write(b"status=success\n")
    self.write(FLUSH_PACKET)

  def getDelayedBlob(self, pathname) -> bytes:
    # If asked for a blob we don't have, return empty
    # This seems to occur when there is a conflicted merge
    if pathname not in self.smudgesAwaitingPickup:
      return b''
    ret = self.smudgesAwaitingPickup[pathname]
    del (self.smudgesAwaitingPickup[pathname])
    return ret

  def filterProcess(self) -> NoReturn:
    """ https://git-scm.com/docs/gitattributes#_long_running_filter_process """
    try:
      self.versionHandshake()
      self.capabilitiesHandshake()

      while True:
        command, pathname, content, candelay = self.readCommand()
        try:
          if command == "clean":
            res = self.clean(pathname, content)
            self.writeSuccess(res)
          elif command == "smudge":
            if candelay:
              self.scheduleSmudge(pathname, content)
              self.writeDelayed()
            elif len(content) == 0:
              res = self.getDelayedBlob(pathname)
              self.writeSuccess(res)
            else:
              res = self.smudge(pathname, content)
              self.writeSuccess(res)
          elif command == "list_available_blobs":
            self.writeListOfAvailableBlobs()
        except Exception as e:
          logger.error(f"Error processing {command} on {pathname}", exc_info=e)
          self.writeError()
          raise
    except EOFError:
      exit(0)
    except:
      self.shutdown(True)
      raise

  def shutdown(self, force=False):
    try:
      self.executor.shutdown(cancel_futures=True, wait=False)  # type: ignore
    except TypeError:  #Python <=3.8 doesn't have cancel_futures
      self.executor.shutdown(wait=False)
    finally:
      if force:
        try:
          # Stop threadpool executors
          import signal
          import os
          os.kill(os.getpid(), signal.SIGTERM)
        except:
          pass


def parseKv(s: bytes) -> Tuple[str, str]:
  [k, v] = s.split(b"=", 1)
  return (k.decode("utf-8"), v.decode("utf-8"))
