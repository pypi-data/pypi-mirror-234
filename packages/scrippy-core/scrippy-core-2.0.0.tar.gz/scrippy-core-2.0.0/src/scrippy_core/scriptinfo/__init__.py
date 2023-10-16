"""The scrippy_core.scriptinfo sub-module."""
import os
import __main__


class ScriptInfo:
  """ScriptInfo object."""

  @staticmethod
  def get_full_filename():
    """Returns current script full path."""
    return __main__.__file__

  @staticmethod
  def get_filename():
    """Returns current script filename."""
    return os.path.basename(__main__.__file__)

  @staticmethod
  def get_name():
    """Returns current script name."""
    return os.path.splitext(ScriptInfo.get_filename())[0]

  @staticmethod
  def get_doc():
    """Returns current script doc string."""
    return __main__.__doc__
