import os
import sys
import logging
import coloredlogs
from scrippy_core.context import GlobalContext
from scrippy_core.logger import ScrippyLogger


class LogManager:
  """The purpose of the ``LogManager`` object is to configure the logger used in the whole **Scrippy** package and all its subpackages.
  """

  terms = ["linux", "xterm", "xterm-256color"]
  console_fmt = '[%(asctime)s] [%(levelname)-8s] %(message)s'
  file_fmt = '[%(asctime)s] [%(levelname)-8s] %(message)s'
  datefmt = '%Y%m%d %H:%M:%S'
  c_field_styles = {'asctime': {'color': 'magenta'},
                    'hostname': {'color': 'magenta'},
                    'levelname': {'bold': True, 'color': 'white'},
                    'programname': {'color': 'cyan'},
                    'name': {'color': 'cyan'}}
  c_level_styles = {'debug': {'color': 'white'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'bold': True, 'color': 'red'}}
  f_field_styles = {'asctime': {'color': 'magenta'},
                    'hostname': {'color': 'magenta'},
                    'levelname': {'color': 'white'},
                    'programname': {'color': 'cyan'},
                    'name': {'color': 'cyan'}}
  f_level_styles = {'debug': {'color': 'white'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'color': 'red'}}

  def __init__(self):
    logging.setLoggerClass(ScrippyLogger)
    self.handlers = {}
    self._set_default()
    self.logger = logging.getLogger("scrippy.main")

  def _set_default(self):
    """Configure the logger default configuration to *stdout*.

    If the ``TERM`` environment variable is defined and is one of "linux", "xterm" or "xterm-256color" the default logger will use ``coloredlogs`` to enhance log readability with colors.

    The default logging level is set to ``INFO``.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    if "TERM" in os.environ and os.environ["TERM"] in self.terms:
      console_handler.setFormatter(
          coloredlogs.ColoredFormatter(fmt=self.console_fmt,
                                       datefmt=self.datefmt,
                                       level_styles=self.c_level_styles,
                                       field_styles=self.c_field_styles))
    else:
      console_handler.setFormatter(logging.Formatter(fmt=self.console_fmt,
                                                     datefmt=self.datefmt))
    logging.basicConfig(level=logging.INFO,
                        handlers=[console_handler])

  def set_log_level(self, level):
    """Set the log level

    Arguments:
      level: A string specifying the desired log level. It **must** be one of the ``logging`` *Python* module standard levels (``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``).

    Raises:
      ``ValueError``: When the given ``level`` is not a valid level name.
    """
    log_levels = {"debug": logging.DEBUG,
                  "info": logging.INFO,
                  "error": logging.ERROR,
                  "critical": logging.CRITICAL,
                  "none": logging.NOTSET}
    self.logger.setLevel(log_levels.get(level))

  def add_file_handler(self, script, session):
    """Adds a file handler to the logger.

    Arguments:
      script: A string specifying script name.
      session: A unique string defining the script execution session.
    """
    log_dname = os.path.join(GlobalContext().get_env().get("logdir"),
                             script)
    os.makedirs(log_dname, exist_ok=True)
    log_fname = os.path.join(log_dname, f"{script}_{session}.log")
    self.handlers[session] = logging.FileHandler(log_fname)
    self.handlers[session].setFormatter(
        coloredlogs.ColoredFormatter(fmt=self.file_fmt,
                                     datefmt=self.datefmt,
                                     level_styles=self.f_level_styles,
                                     field_styles=self.f_field_styles))
    self.logger.addHandler(self.handlers[session])

  def remove_file_handler(self, session):
    """Removes the file handler associated with the specified session.

    Arguments:
      session: A unique string specifying a script session.
    """
    self.logger.removeHandler(self.handlers[session])

  @staticmethod
  def print_logfile(script, session):
    """Print to *stdout* the log file content for the specified script session.

    Arguments:
      script: A string specifying the script name.
      session: A unique string defining the script execution session to retrieve the log for
    """
    log_dname = os.path.join(GlobalContext().get_env().get("logdir"),
                             script)
    log_fname = os.path.join(log_dname, f"{script}_{session}.log")
    with open(log_fname, "r", encoding="utf-8") as log:
      print(log.read())
