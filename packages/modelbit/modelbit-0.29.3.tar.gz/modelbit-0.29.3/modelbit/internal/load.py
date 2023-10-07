from typing import Optional
from modelbit.helpers import InstancePickleWrapper
import sys


def loadFromPickle(data: bytes, restoreClass: Optional[type] = None):
  import pickle
  import __main__ as main_package  # Required to load pickles
  try:
    value = pickle.loads(data)
  except ModuleNotFoundError as e:
    if e.name is None:
      raise
    # If someone is trying to load a training job result in a notebook
    # they might have the class defined locally.
    # If so, try loading the pickle with the class in main.
    sys.modules[e.name] = sys.modules['__main__']
    try:
      value = pickle.loads(data)
    finally:
      del sys.modules[e.name]

  if restoreClass is not None and isinstance(value, InstancePickleWrapper):
    return value.restore(restoreClass)
  else:
    return value
