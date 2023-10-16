import os
import errno
from filelock import FileLock


class PIDStack:
  """The PIDStack class allows for the management of concurrent executions."""

  def __init__(self, name, tmpdir):
    self.stack_file_path = os.path.join(tmpdir, f"{name}.pids")
    self.lock = FileLock(f"{self.stack_file_path}.lock")

  def _read(self):
    pids = []
    if os.path.isfile(self.stack_file_path):
      with open(self.stack_file_path, mode="r", encoding="utf-8") as stack_file:
        pids = [pid.strip() for pid in stack_file.readlines()]
      if pids is None:
        pids = []
    return pids

  def _write(self, pids):
    with open(self.stack_file_path, mode="w", encoding="utf-8") as stack_file:
      for pid in pids:
        stack_file.write(f"{pid}\n")

  def get_pids(self):
    """Returns the list of PIDs in queue or currently executing."""
    pids = []
    with self.lock.acquire():
      for pid in self._read():
        try:
          os.kill(int(pid), 0)
          pids.append(int(pid))
        except OSError as e:
          if e.errno == errno.EPERM:
            pids.append(pid)
          elif e.errno == errno.ESRCH:
            pass
      self._write(pids)
      return pids

  def register(self):
    """Registers a new PID in the stack"""
    with self.lock.acquire():
      pids = self.get_pids()
      pids.append(os.getpid())
      self._write(pids)

  def checkout(self):
    """Cleans the stack."""
    with self.lock.acquire():
      self._write([pid for pid in self.get_pids() if pid != str(os.getpid())])
