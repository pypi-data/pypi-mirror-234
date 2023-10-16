
import re


class Vault:
  """The Vault class manages sensitive information that should not appear in logs."""

  def __init__(self):
    self.secrets = []
    self.pattern = None

  def add(self, secret):
    if not self.is_secret(value=str(secret)):
      self.secrets.append(str(secret))
    self.pattern = re.compile(f"{'|'.join(self.secrets)}")

  def is_secret(self, value):
    return str(value) in self.secrets

  def protect(self, msg):
    if self.pattern is not None:
      return re.sub(self.pattern, "*******", str(msg))
    return msg
