import os
import time


class GlobalContext:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(GlobalContext, cls).__new__(cls)
      cls._instance._set_session()
      cls._instance.set_env(None)
      cls._instance.set_context(None)
      cls._instance.set_full_filename(None)
      cls._instance.set_filename(None)
      cls._instance.set_name(None)
      cls._instance.set_log_manager(None)
      cls._instance.set_logger(None)
    return cls._instance

  def _set_session(self):
    self.session = f"{time.time()}_{os.getpid()}"

  def get_session(self):
    return self.session

  def set_env(self, env):
    self.env = env

  def get_env(self):
    return self.env

  def set_context(self, context):
    self.context = context

  def get_context(self):
    return self.context

  def set_full_filename(self, filename):
    self.full_filename = filename

  def get_full_filename(self):
    return self.full_filename

  def set_filename(self, filename):
    self.filename = filename

  def get_filename(self):
    return self.filename

  def set_name(self, name):
    self.name = name

  def get_name(self):
    return self.name

  def set_log_manager(self, log_manager):
    self.log_manager = log_manager

  def get_log_manager(self):
    return self.log_manager

  def set_logger(self, logger):
    self.logger = logger

  def get_logger(self):
    return self.logger
