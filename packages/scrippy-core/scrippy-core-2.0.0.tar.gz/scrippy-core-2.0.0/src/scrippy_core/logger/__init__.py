import logging
from scrippy_core.vault import Vault


class ScrippyLogger(logging.Logger):
  """The ``ScrippyLogger`` class overrides the ``logging.Logger`` class.

  It adds a ``scrippy_core.vault.Vault`` instance to the logger object allowing secret management.

  Any secret stored in the vault instance will be redacted before logging.
  """
  def __init__(self, name, level=logging.NOTSET):
    super().__init__(name, level)
    self.vault = Vault()
    self.name = name

  def add_secret(self, secret):
    self.vault.add(secret=secret)

  def log_line(self, level=logging.INFO):
    self.log(level=level, msg="-" * 80)

  def log_section(self, prefix, message, level=logging.INFO):
    self.log_line(level=level)
    self.log(level=level, msg=f"[{prefix}] {message}")
    self.log_line(level=level)

  def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
    """Override logging.Logger.makeRecord.
    """
    if self.vault is not None:
      msg = self.vault.protect(msg)
    return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
