"""The scrippy_core.workspace sub-module provides the necessary objects for workspace management."""
import os
import shutil
import pathlib
from scrippy_core.context import GlobalContext
from scrippy_core.error_handler import ScrippyCoreError


class Workspace:
  """The Workspace class provides a workspace with a directory based on the name passed as an argument to the constructor.

  The workspace will be created in the SCRIPPY_TMPDIR directory."""

  def __init__(self, name):
    env = GlobalContext().get_env()
    self.logger = GlobalContext().get_logger()
    self.path = pathlib.Path(os.path.join(env.get("tmpdir"), name))

  def __enter__(self):
    """Entry point"""
    self.logger.info(f"[+] Using workspace: {self.path}")
    try:
      self.path.mkdir(mode=0o750, parents=True, exist_ok=False)
    except Exception as err:
      err_msg = f"Unable to create workspace: [{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    return str(self.path)

  def __exit__(self, kind, value, traceback):
    """Exit point."""
    self.logger.info(f"[+] Workspace deletion: {self.path}")
    try:
      shutil.rmtree(self.path)
    except Exception as err:
      err_msg = f"Error while deleting workspace: [{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def __eq__(self, other):
    """Override default implementation."""
    if isinstance(other, Workspace):
      return self.path == other.path
    return False

  def __str__(self):
    return str(self.path)
