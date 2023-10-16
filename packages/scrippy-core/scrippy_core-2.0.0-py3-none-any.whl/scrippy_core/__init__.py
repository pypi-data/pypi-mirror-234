"""Scrippy Core module."""
import os
import grp
import pwd
import time
import yaml
import logging
from scrippy_core.conf import Config
from scrippy_core import error_handler
from scrippy_core.stack import PIDStack
from scrippy_core.history import History
from scrippy_core.arguments import Parser
from scrippy_core.workspace import Workspace
from scrippy_core.scriptinfo import ScriptInfo
from scrippy_core.logger.manager import LogManager
from scrippy_core.error_handler import ScrippyCoreError
from scrippy_core.context import GlobalContext

# ------------------------------------------------------------------------------
# INITIALIZATION
# ------------------------------------------------------------------------------
# Different levels of configuration files:
# - Vendor configuration file: /etc/scrippy/scrippy.yml
# - User configuration file: ~/.config/scrippy/scrippy.yml
# - SysAdmin configuration file: /usr/local/etc/scrippy/scrippy.yml
#
# Precedence:
# -----------
# SysAdmin values can not be overriden by user
# User values override Vendor values
#
conf_files = ["/etc/scrippy/scrippy.yml",
              os.path.expanduser("~/.config/scrippy/scrippy.yml"),
              "/usr/local/etc/scrippy/scrippy.yml"]

# Scrippy environment vars
env = {"logdir": None,
       "histdir": None,
       "reportdir": None,
       "tmpdir": None,
       "datadir": None,
       "templatedir": None,
       "confdir": None}

for conf_file in conf_files:
  if os.path.isfile(conf_file):
    with open(conf_file, mode="r", encoding="utf-8") as conf_file:
      scrippy_conf = yaml.load(conf_file, Loader=yaml.FullLoader)
      env["logdir"] = scrippy_conf.get("env").get("logdir")
      env["histdir"] = scrippy_conf.get("env").get("histdir")
      env["reportdir"] = scrippy_conf.get("env").get("reportdir")
      env["tmpdir"] = scrippy_conf.get("env").get("tmpdir")
      env["datadir"] = scrippy_conf.get("env").get("datadir")
      env["templatedir"] = scrippy_conf.get("env").get("templatedir")
      env["confdir"] = scrippy_conf.get("env").get("confdir")

for key, value in env.items():
  if value is None:
    raise ScrippyCoreError(f"Missing configuration key: {key}")

log_manager = LogManager()
logger = logging.getLogger("scrippy.main")
GlobalContext().set_env(env=env)
GlobalContext().set_logger(logger=logger)
GlobalContext().set_name(name=ScriptInfo().get_name())
GlobalContext().set_full_filename(filename=ScriptInfo().get_full_filename())
GlobalContext().set_filename(filename=ScriptInfo().get_filename())
GlobalContext().set_log_manager(log_manager=log_manager)
arg_parser = Parser()
if arg_parser.args.no_stdout:
  log_manager.set_log_level("error")
if arg_parser.args.debug:
  log_manager.set_log_level("debug")
arg_parser.register_secrets()


class ScriptContext:
  """Script execution context."""
  def __init__(self, retention=50, workspace=True):
    self.logger = logger
    self.filename = ScriptInfo.get_filename()
    self.name = ScriptInfo.get_name()
    self.retention = retention
    self.workspace_enabled = workspace
    self.args = arg_parser.args
    self.config = None
    self.history = None
    self.workspace = None
    self.workspace_path = None
    self.pidstack = None

  def __enter__(self):
    """Entry point."""
    self.config = Config()
    if self.config.has(section="log", key="level"):
      log_manager.set_log_level(level=self.config.get('log', 'level').lower())
    self.config.register_secrets()
    self.check_users()
    self.check_groups()
    self.stack()
    self.check_instances()
    if arg_parser.args.no_log_file:
      self.logger.warning("[+] Option --no-log-file is set -> This session will not be logged nor recorded into history")
    else:
      log_manager.add_file_handler(script=self.name,
                                   session=GlobalContext().get_session())
      self.history = History(retention=self.retention)
    if self.workspace_enabled:
      workspace_name = f"{self.name}_{GlobalContext().get_session()}"
      self.workspace = Workspace(name=workspace_name)
    if self.history is not None:
      self.history.__enter__()
    if self.workspace is not None:
      self.workspace_path = self.workspace.__enter__()
    return self

  def __exit__(self, kind, value, tb):
    """Exit point."""
    if self.workspace is not None:
      self.workspace.__exit__(kind, value, tb)
    if self.history is not None:
      self.history.__exit__(kind, value, tb)
    self.unstack()
    error_handler.handle_error(kind, value, tb)

  def check_users(self):
    """
    Checks if the current user is authorized to execute the script by comparing the "@user" declarations in the script's header.

    Raises a ScrippyCoreError if the user is not authorized.
    """
    doc = ScriptInfo().get_doc()
    user_id = os.geteuid()
    try:
      users = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@user")]
      users = [pwd.getpwnam(user).pw_uid for user in users]
      if len(users) > 0 and user_id not in users:
        raise ScrippyCoreError('[BadUserError] Unauthorized user')
    except KeyError as err:
      raise ScrippyCoreError(f"[UnknownUserError] Unknown user: {str(err)}") from err
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def check_groups(self):
    """
    Verifies that the current user is authorized to execute the script by comparing the "@group" declarations in the script's header.

    Raises a ScrippyCoreError if the user is not part of the authorized groups.
    """
    doc = ScriptInfo().get_doc()
    user_groups = os.getgroups()
    try:
      groups = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@group")]
      groups = [grp.getgrnam(group)[2] for group in groups]
      if len(groups) > 0:
        if not len([groups for g in user_groups if g in groups]) > 0:
          raise ScrippyCoreError("[BadGroupError] User is not member of an authorized group")
    except KeyError as err:
      raise ScrippyCoreError(f"[UnknownGroupError] Unknown group: {str(err)}") from err
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def check_instances(self):
    """
    Verifies that the maximum number of allowed instances to be simultaneously executed is not reached by comparing the declaration @max_instance in the script's header with the number of PIDs returned by the pidstack.

    If the maximum instance limit is reached, the script will pause until the number of currently running instances is lower than the allowed number of instances.

    When the maximum allowed instances are not reached, the script registers itself in the pidstack and proceeds with execution.
    """
    doc = ScriptInfo().get_doc()
    sleep_step = 3
    bools = ["true", "1", "on"]
    try:
      max_instance = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@max_instance")][0]
    except IndexError:
      max_instance = 0
    try:
      timeout = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@timeout")][0]
    except IndexError:
      timeout = 0
    try:
      exit_on_wait = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@exit_on_wait")][0]
    except IndexError:
      exit_on_wait = "False"
    try:
      exit_on_timeout = [line.split(':')[1].strip() for line in doc.splitlines() if line.strip().startswith("@exit_on_timeout")][0]
    except IndexError:
      exit_on_timeout = "False"
    pids = self.pidstack.get_pids()
    try:
      timeout = int(timeout)
      max_instance = int(max_instance)
      exit_on_timeout = exit_on_timeout.lower() in bools
      exit_on_wait = exit_on_wait.lower() in bools
      if max_instance > 0 and len(pids) > max_instance:
        self.logger.info(f"[+] Waiting for an execution slot: {len(pids)}/{max_instance} [{timeout}s]")
        while len(pids) > max_instance and pids[0] != os.getpid():
          timeout -= sleep_step
          if timeout <= 0 and exit_on_timeout:
            raise ScrippyCoreError("TimeoutError: Timeout expired")
          if exit_on_wait:
            raise ScrippyCoreError(f"EagernessError: `exit_on_wait` is set to {exit_on_wait}")
          pids = self.pidstack.get_pids()
          time.sleep(sleep_step)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def stack(self):
    try:
      self.pidstack = PIDStack(name=self.name,
                               tmpdir=GlobalContext().get_env().get("tmpdir"))
      self.pidstack.register()
    except PermissionError as err:
      err_msg = f"Error while creating instances stack: [{err.__class__.__name__}] {err}"
      self.logger.critical(err_msg)
      raise err

  def unstack(self):
    self.pidstack.checkout()
