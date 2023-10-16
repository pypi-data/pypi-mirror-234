import logging
import logging.handlers
import os
import sys
import traceback
from functools import wraps
from typing import Callable, List, Optional, TypeVar, Union, cast
import datetime

from modelbit.api.api import MbApi  # For perf, skip __init__
from modelbit.error import ModelbitError, UserFacingError
from modelbit.utils import inDeployment
from modelbit.ux import printTemplate

logger = logging.getLogger(__name__)


def enableFileLogging():
  return os.environ.get("MB_LOG", None) is not None


def initLogging():
  LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
  streamHandler = logging.StreamHandler()
  handlers: List[logging.Handler] = [streamHandler]
  streamHandler.setLevel(LOGLEVEL)
  if enableFileLogging():
    try:
      import appdirs
      logDir = appdirs.user_log_dir("modelbit")
      if not os.path.exists(logDir):
        os.makedirs(logDir, exist_ok=True)
      fileHandler = logging.handlers.RotatingFileHandler(os.path.join(logDir, "log.txt"),
                                                         maxBytes=10485760,
                                                         backupCount=5)
      fileHandler.setLevel(level="INFO")
      handlers.append(fileHandler)
    except Exception as e:
      print(e)
      logging.info(e)

  logging.basicConfig(level="INFO", handlers=handlers)


def logErrorToWeb(mbApi: Optional[MbApi], userErrorMsg: str):
  errStack = traceback.format_exception(*sys.exc_info())[1:]
  errStack.reverse()
  errorMsg = userErrorMsg + "\n" + "".join(errStack)

  if inDeployment():
    print(errorMsg, file=sys.stderr)  # TODO: Maybe report these to web?
    return

  from modelbit.api import MbApi
  mbApi = mbApi or MbApi()
  try:
    localnow = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()
    mbApi.getJson("api/cli/v1/error", {"errorMsg": errorMsg, "now": localnow})
  except Exception as e:
    logger.info(e)


T = TypeVar("T")


def eatErrorAndLog(mbApi: Optional[MbApi], genericMsg: str):

  def decorator(func: Callable[..., T]) -> Callable[..., T]:

    @wraps(func)
    def innerFn(*args: object, **kwargs: object) -> T:
      error: Optional[Union[Exception,
                            str]] = None  # Store and raise outside the handler so the trace is more compact.
      try:
        return func(*args, **kwargs)
      except (KeyError, TypeError) as e:
        logErrorToWeb(mbApi, f"{genericMsg}, {type(e)}, {str(e)}")
        error = e
      except UserFacingError as e:
        if e.logToModelbit:
          logErrorToWeb(mbApi, e.userFacingErrorMessage)
        printTemplate("error", None, errorText=genericMsg + " " + e.userFacingErrorMessage)
        error = cast(str, e.userFacingErrorMessage)
      except Exception as e:
        specificError = cast(Optional[str], getattr(e, "userFacingErrorMessage", None))
        error = genericMsg + (" " + specificError if specificError is not None else "")
        logErrorToWeb(mbApi, cast(str, error))
        printTemplate("error_details", None, errorText=error, errorDetails=traceback.format_exc())
      # Convert to generic ModelbitError.
      if type(error) == str:
        raise ModelbitError(error)
      else:
        raise cast(Exception, error)

    return innerFn

  return decorator
