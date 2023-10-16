from argparse import Action, SUPPRESS
from scrippy_core.history import History
from scrippy_core.context import GlobalContext


class LogAction(Action):
  def __init__(self,
               option_strings,
               dest=SUPPRESS,
               default=SUPPRESS,
               help="Show execution history"):
    super(LogAction, self).__init__(option_strings=option_strings,
                                    dest=dest,
                                    default=default,
                                    nargs='?',
                                    type=str,
                                    metavar=('SESSION (default: last)'),
                                    help=help)

  def __call__(self, parser, namespace, session, option_string=None):
    session = session or History().get_last_session()
    GlobalContext().get_log_manager().print_logfile(GlobalContext().get_name(),
                                                    session)
    parser.exit()
