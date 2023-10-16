"""The scrippy_core.arguments sub-module provides all the necessary objects and functions for handling arguments passed to the scripts."""
import argparse
import argcomplete
from scrippy_core.scriptinfo import ScriptInfo
from scrippy_core.context import GlobalContext
from scrippy_core.arguments.logaction import LogAction
from scrippy_core.error_handler import ScrippyCoreError
from scrippy_core.arguments.sourceaction import SourceAction
from scrippy_core.arguments.historyaction import HistoryAction


class Parser:
  """The Parser class enables the analysis of arguments passed to the scripts."""

  def __init__(self):
    """Parser instantiation."""
    self.logger = GlobalContext().get_logger()
    self.required = {'true': True, 'false': False}
    self.parser = argparse.ArgumentParser(prog=ScriptInfo.get_filename(),
                                          formatter_class=argparse.RawTextHelpFormatter)
    self._add_default_args()
    self._add_args()
    argcomplete.autocomplete(self.parser)
    self.args = self.parser.parse_args()
    self._check_implies(self.args)
    self._check_conflicts(self.args)

  def _get_description(self):
    try:
      description = [line.split(':')[1].strip() for line in ScriptInfo.get_doc().splitlines() if line.strip().startswith("@description")]
      return description[0]
    except IndexError as err:
      err_msg = "Missing script description"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def _get_author(self):
    try:
      author = [line.split(':')[1].strip() for line in ScriptInfo.get_doc().splitlines() if line.strip().startswith("@author")]
      return author[0]
    except IndexError as err:
      err_msg = "Missing script author"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def _get_version(self):
    try:
      version = [line.split(':')[1].strip() for line in ScriptInfo.get_doc().splitlines() if line.strip().startswith("@version")]
      return version[0]
    except IndexError as err:
      err_msg = "Missing script version"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def _get_date(self):
    try:
      date = [line.split(':')[1].strip() for line in ScriptInfo.get_doc().splitlines() if line.strip().startswith("@date")]
      return date[0]
    except IndexError as err:
      err_msg = "Missing script date"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def _get_args(self):
    s_args = [line.split(':')[1].strip() for line in ScriptInfo.get_doc().splitlines() if line.strip().startswith("@args")]
    try:
      args = []
      for arg in s_args:
        arg = arg.split('|')
        n_arg = {'name': arg[0],
                 'type': arg[1],
                 'help': arg[2],
                 'nargs': arg[3],
                 'default': arg[4],
                 'conflicts': arg[5],
                 'implies': arg[6],
                 'required': arg[7]
                 }
        try:
          n_arg['secret'] = arg[8]
        except IndexError:
          n_arg['secret'] = 'false'
        args.append(n_arg)
      return args
    except Exception as err:
      err_msg = f"Arguments declaration error: [{err.__class__.__name__}]: {err}"
      self.logger.critical(err_msg)
      raise ScrippyCoreError(err_msg) from err

  def _add_default_args(self):
    self.parser.description = f"Author: {self._get_author()}\nDate: {self._get_date()}\nVersion: {self._get_version()}\nDescription: {self._get_description()}"
    self.parser.add_argument('--version', help='Show version and exit', action='version', version=f'%(prog)s {self._get_version()}')
    self.parser.add_argument('--source-code', help='Show source code', action=SourceAction)
    self.parser.add_argument('--hist', help='Show execution history', action=HistoryAction)
    self.parser.add_argument('--log', help='Show log content', action=LogAction)
    self.parser.add_argument('--debug', help='Force log level to DEBUG', action='store_true')
    self.parser.add_argument('--no-stdout', help='Disable log output to standard output (error et critical are kept)', action='store_true')
    self.parser.add_argument('--no-log-file', help='disable log file and history', action='store_true')

  def _add_args(self):
    types = {'str': (self._store, str),
             'int': (self._store, int),
             'float': (self._store, float),
             'choice': (self._store_choice, list),
             'bool': (self._store_bool, bool)
             }
    args = self._get_args()
    for arg in args:
      try:
        types[arg['type']][0](arg, types[arg['type']][1])
      except Exception as err:
        self.logger.critical(f"Arg: {arg}")
        err_msg = f"Arguments declaration error: [{err.__class__.__name__}]: {err}"
        self.logger.critical(err_msg)
        raise ScrippyCoreError(err_msg) from err

  def _store(self, arg, arg_type=str):
    if len(arg['nargs']) > 0:
      try:
        arg['nargs'] = int(arg['nargs'])
      except ValueError as e:
        if arg['nargs'] not in ['+', '?']:
          raise e

    options = {'help': arg['help'],
               'action': 'store',
               'type': arg_type,
               'required': self.required[arg['required'].lower()]}

    if arg['default']:
      options['default'] = arg['default']
    if arg['nargs'] != 1:
      options['nargs'] = arg['nargs']
      if arg['default']:
        options['default'] = arg['default'].split(',')

    self.parser.add_argument(f"--{arg['name']}", **options)

  def _store_bool(self, arg, arg_type=bool):
    store_type = {'false': 'store_true', 'true': 'store_false'}
    if not len(arg['default']) > 0:
      arg['default'] = 'false'
    self.parser.add_argument(f"--{arg['name']}",
                             help=arg['help'],
                             action=store_type[arg['default'].lower()],
                             required=self.required[arg['required'].lower()])

  def _store_choice(self, arg, arg_type=list):
    self.parser.add_argument(f"--{arg['name']}",
                             choices=arg['default'].split(','),
                             help=arg['help'],
                             required=self.required[arg['required'].lower()])

  def _check_implies(self, args):
    declared_arg_imps = filter(lambda arg: arg['implies'], self._get_args())
    for arg in declared_arg_imps:
      arg_name = arg['name']
      for imp in arg['implies'].split(','):
        dict_args = vars(args)
        if dict_args[arg_name] and not dict_args[imp]:
          self.parser.error(f"Params --{arg_name} implies --{imp}. Please add --{imp}")

  def _check_conflicts(self, args):
    declared_arg_conflicts = filter(lambda arg: arg['conflicts'], self._get_args())
    for arg in declared_arg_conflicts:
      arg_name = arg['name']
      for conflict_arg in arg['conflicts'].split(','):
        dict_args = vars(args)
        if dict_args[arg_name] and dict_args[conflict_arg]:
          self.parser.error(f"Params --{arg_name} conflicts with --{conflict_arg}. Please remove --{arg_name} or --{conflict_arg}")

  def register_secrets(self):
    self.logger.info("[+] Secrets registration (args)")
    declared_arg_secrets = filter(lambda arg: arg['secret'], self._get_args())
    for arg in declared_arg_secrets:
      if arg["secret"].lower() == "true":
        self.logger.add_secret(secret=getattr(self.args, arg["name"]))
