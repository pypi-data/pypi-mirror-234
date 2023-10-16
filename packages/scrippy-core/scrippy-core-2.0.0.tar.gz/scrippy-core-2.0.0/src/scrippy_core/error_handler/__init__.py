"""Error management."""
import sys
import logging
import traceback
from scrippy_core.context import GlobalContext


class ScrippyCoreError(Exception):
  """Specific class of error."""

  def __init__(self, message):
    self.message = message
    super().__init__(self.message)


def handle_error(kind, value, tb):
  """Trap all errors and quit gracefully after all errors are logged."""
  if kind is not None:
    logger = GlobalContext().get_logger()
    logger.critical(f"[{kind.__name__}]: {str(value)}")
    if logger.getEffectiveLevel() <= logging.DEBUG:
      traceback.print_tb(tb)
    if kind != SystemExit:
      sys.exit(1)
