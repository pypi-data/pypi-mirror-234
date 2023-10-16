"""Display script source."""
from rich.console import Console
from rich.syntax import Syntax
from argparse import Action, SUPPRESS
from scrippy_core.scriptinfo import ScriptInfo


class SourceAction(Action):
  """Class for code source display."""
  def __init__(self, option_strings, dest=SUPPRESS, default=SUPPRESS, help="Show source code"):
    super(SourceAction, self).__init__(option_strings=option_strings,
                                       dest=dest,
                                       default=default,
                                       nargs=0,
                                       type=bool,
                                       help=help)

  def __call__(self, parser, namespace, nb_execution, option_string=None):
    console = Console()
    syntax = Syntax.from_path(ScriptInfo.get_full_filename(), line_numbers=True)
    console.print(syntax)
    parser.exit()
