import logging
import os
import time
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

from modelbit.error import NonRetryableError, UserFacingError
from modelbit.telemetry import logErrorToWeb
from modelbit.api import MbApi

T = TypeVar("T")


def retry(retries: int, logger: Optional[logging.Logger]):

  def decorator(func: Callable[..., T]) -> Callable[..., T]:
    if os.getenv("NORETRY", None):
      return func

    @wraps(func)
    def innerFn(*args: Any, **kwargs: Any):
      lastError: Optional[Exception] = None
      for attempt in range(retries):
        try:
          return func(*args, **kwargs)
        except NonRetryableError:
          raise
        except UserFacingError:
          raise
        except Exception as e:
          if logger:
            logger.info("Retrying:  got %s", e)
          if isinstance(args[0], MbApi):
            logErrorToWeb(args[0], str(e))
          else:
            logErrorToWeb(None, str(e))
          lastError = e
          retryTime = 2**attempt
          if logger and attempt > 2:
            logger.warning("Retrying in %ds: %s", retryTime, str(e))
          time.sleep(retryTime)
      if lastError is None:
        raise Exception(f"Failed after {retries} retries. Please contact support.")
      raise lastError

    return innerFn

  return decorator
