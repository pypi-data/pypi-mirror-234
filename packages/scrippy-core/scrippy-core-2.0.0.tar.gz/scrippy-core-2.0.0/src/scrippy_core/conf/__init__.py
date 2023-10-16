"""
This module provides an interface for configuring scripts based on the Scrippy framework.

This interface allows for:
- Loading and automatic consideration of a configuration file
- Verification of configuration validity
"""

import os
import configparser
from scrippy_core.scriptinfo import ScriptInfo
from scrippy_core.error_handler import ScrippyCoreError
from scrippy_core.context import GlobalContext


class Config:
  """
  Config is the main class of the scrippy_core.conf module.

  It allows for the automatic loading of the configuration and, if the script's docstring includes a set of lines starting with @conf, it enables the validation of the configuration from the configuration file.

  The lines in the configuration format declarations must adhere to the following format:

  @conf:<section>|<key>|<value_type>

  <value_type> must be one of the following recognized types:

      str (string)
      int (integer)
      float (floating-point number)
      bool (boolean)

  Example:
  --------
  Starting from the following declaration:

  @conf:log/level/str
  @conf:database/port/int
  @conf:sql/verbose/bool

  The following configuration will be checked:
  [log]
    level = ERROR
  [database]
    port = 5432
  [sql]
    verbose = True
  """

  def __init__(self):
    """Initialise l'instance.

    No validation of parameter values is performed.
    Only the configuration structure (presence of sections and keys described by the @conf set) is checked. Validation of the declared key types is also performed.
    """
    env = GlobalContext().get_env()
    self.logger = GlobalContext().get_logger()
    self.conf = configparser.ConfigParser()
    self.context = GlobalContext().get_context()
    self.doc = ScriptInfo().get_doc()
    conf_fname = f"{ScriptInfo().get_name()}.conf"
    self.config_filename = os.path.join(env.get("confdir"), conf_fname)
    if os.path.isfile(self.config_filename):
      self.logger.info(f"[+] Loading configuration file {self.config_filename}")
      self.conf.read(self.config_filename)
    else:
      self.logger.info(f"[+] No configuration file {self.config_filename}")
    self._check()

  def _check(self):
    """
    Configuration check.

    This method is automatically called by the constructor if the optional 'params' argument is provided. This method should not be called other than by the constructor of the Config class.
    """
    self.logger.info("[+] Configuration check")
    conf_lines = []
    conf_lines = [line.split(':')[1].strip() for line in self.doc.splitlines() if line.strip().startswith("@conf")]
    for line in conf_lines:
      try:
        section, key, param_type, secret = line.split("|")
        value = self.get(section, key, param_type)
        if secret.lower() == "true":
          self.logger.add_secret(secret=value)
      except ValueError:
        section, key, param_type = line.split("|")
        value = self.get(section, key, param_type)
      self.logger.debug(f"[{section}][{key}] = {value} [OK]")
    return True

  def register_secrets(self):
    self.logger.info("[+] Secrets registration (conf)")
    conf_lines = []
    conf_lines = [line.split(':')[1].strip() for line in self.doc.splitlines() if line.strip().startswith("@conf")]
    for line in conf_lines:
      try:
        section, key, param_type, secret = line.split("|")
        value = self.get(section, key, param_type)
        if secret.lower() == "true":
          self.logger.add_secret(secret=value)
      except ValueError:
        pass

  def get_section(self, section):
    """
    Returns the set of key/value pairs for the section passed as an argument.
    Raises an exception if the requested section does not exist.
    """
    sec = {}
    try:
      for key in self.conf[section]:
        sec[key] = self.conf[section][key]
      return sec
    except configparser.NoSectionError as err:
      err_msg = f"Missing or unknown configuration section: [{section}]"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def get(self, section, key, param_type='str'):
    """
    Returns the value of a key from the key name and section passed as arguments.

    Unless the 'param_type' parameter is set to one of the allowed values (str by default, int, float, or bool), the returned type is always a string.
    """
    try:
      return {'int': self.conf.getint,
              'float': self.conf.getfloat,
              'bool': self.conf.getboolean,
              'str': self.conf.get}[param_type](section, key)
    except configparser.NoOptionError as err:
      err_msg = f"Missing or unknown configuration parameter: [{section}][{key}]"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except configparser.NoSectionError as err:
      err_msg = f"Missing or unknown configuration section: [{section}]"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except ValueError as err:
      err_msg = f"Type error: [{section}][{key}] is not of type '{param_type}'"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err
    except KeyError as err:
      err_msg = f"Usage error: Unknown parameter type: '{param_type}'"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def has(self, section, key):
    """Returns True if the key section.key exists in the configuration."""
    return self.conf.has_option(section, key)
