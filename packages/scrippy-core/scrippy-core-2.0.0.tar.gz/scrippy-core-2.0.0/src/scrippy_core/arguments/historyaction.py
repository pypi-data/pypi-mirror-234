"""Execution history management."""
import sys
from argparse import Action, SUPPRESS
from scrippy_core.history import History
from scrippy_core.context import GlobalContext


class HistoryAction(Action):
  """Management class for execution history."""
  def __init__(self, option_strings,
               dest=SUPPRESS, default=SUPPRESS,
               help="Show execution history"):
    super(HistoryAction, self).__init__(option_strings=option_strings,
                                        dest=dest,
                                        default=default,
                                        nargs='?',
                                        type=int,
                                        # Default max execution saved
                                        const=10,
                                        metavar=('NB_EXECUTION (default:10)'),
                                        help=help)

  def __call__(self, parser, namespace, nb_execution, option_string=None):
    print(f"{nb_execution} last executions of {GlobalContext().get_filename()}")
    formatter = parser._get_formatter()
    formatter.add_text(History().read_history(nb_execution))
    parser._print_message(formatter.format_help(), sys.stdout)
    parser.exit()
