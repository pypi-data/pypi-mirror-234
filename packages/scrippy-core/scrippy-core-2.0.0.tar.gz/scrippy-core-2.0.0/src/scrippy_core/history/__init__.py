"""The scrippy_core.history sub-module provides the necessary objects for managing execution history."""
import os
import sys
import time
import sqlite3
import getpass
from datetime import datetime
from prettytable import PrettyTable
from scrippy_core.context import GlobalContext


class History:
  """L'objet History est l'objet qui fournit l'ensemble des méthodes permettant historisation des executions."""
  def __init__(self, retention=90):
    self.logger = GlobalContext().get_logger()
    self.logger.info(f"[+] Opening history (retention={retention})")
    env = GlobalContext().get_env()
    self.session = GlobalContext().get_session()
    self.retention = retention
    history_db = f"{GlobalContext().get_name()}.db"
    self.hist_filename = os.path.join(env.get("histdir"), history_db)
    self.user_exec = getpass.getuser()
    self.start = time.time()
    self.user_origin = os.getenv("SUDO_USER") or getpass.getuser()
    self.params = sys.argv[1:]

  def __enter__(self):
    """Entry point."""
    if os.path.isfile(self.hist_filename):
      self.purge_old_history()
    else:
      self.create_history()
    session_exec_params = [self.session,
                           self.start,
                           self.user_origin,
                           self.user_exec,
                           str(self.params)]
    with sqlite3.connect(self.hist_filename) as conn:
      cursor = conn.cursor()
      cursor.execute("insert into executions (session, start, origin, exec, params) values (?, ?, ?, ?, ?)", session_exec_params)
      conn.commit()

  def __exit__(self, kind, value, traceback):
    """Exit point."""
    exit_code = 0
    if kind == SystemExit:
      if value.code is not None:
        exit_code = value.code
    elif kind is not None:
      exit_code = kind.__name__
    self.close_history(exit_code)

  def create_history(self):
    with sqlite3.connect(self.hist_filename) as conn:
      cursor = conn.cursor()
      cursor.execute("CREATE TABLE executions (session TEXT, start REAL, end REAL, duration REAL, origin TEXT, exec TEXT, code TEXT, params TEXT, exit_code INTEGER)")
      conn.commit()

  def purge_old_history(self):
    """Purges the history file."""
    with sqlite3.connect(self.hist_filename) as conn:
      cursor = conn.cursor()
      cursor.execute("delete from executions where session not in (select session from executions order by end DESC limit ?)", [self.retention])
      conn.commit()

  def close_history(self, exit_code):
    """Record session exit code and duration."""
    end = time.time()
    delta = datetime.fromtimestamp(end) - datetime.fromtimestamp(self.start)
    result = [end,
              self._format_time_delta(delta),
              exit_code,
              self.session]
    with sqlite3.connect(self.hist_filename) as conn:
      cursor = conn.cursor()
      cursor.execute("update executions set end=?, duration=?, exit_code=? where session=?", result)
      conn.commit()
    self.logger.info(f"[+] End: {exit_code}")

  def get_last_session(self):
    if os.path.isfile(self.hist_filename):
      with sqlite3.connect(self.hist_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("select session from executions order by start desc limit 1")
        return cursor.fetchone()[0]
    return None

  def read_history(self, nb_execution):
    """Read and displays history."""
    if os.path.isfile(self.hist_filename):
      table = PrettyTable()
      table.field_names = ["Session",
                           "Start",
                           "End",
                           "Duration",
                           "Origin",
                           "Exec",
                           "Code",
                           "Params",
                           "Exit"]
      with sqlite3.connect(self.hist_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("select * from executions order by start desc limit ?", [nb_execution])
        sessions = []
        for session in cursor.fetchall():
          sessions.append(self._get_human_readable_dates(session))
        table.add_rows(sessions)
        return table.get_string()
    return None

  def _get_human_readable_dates(self, session):
    """Return session records with human readable start and end time"""
    session = list(session)
    session[1] = datetime.fromtimestamp(session[1]).strftime("%d/%m/%Y %H:%M:%S")
    session[2] = datetime.fromtimestamp(session[2]).strftime("%d/%m/%Y %H:%M:%S")
    return session

  def _format_time_delta(self, tdelta):
    """Take a timedelta object and formats it for humans.
    From https://gist.github.com/dhrrgn/7255361
    """
    delta = dict(days=tdelta.days)
    delta["hrs"], rem = divmod(tdelta.seconds, 3600)
    delta["min"], delta["sec"] = divmod(rem, 60)
    if delta["min"] == 0:
      fmt = "{sec} sec"
    elif delta["hrs"] == 0:
      fmt = "{min} min {sec} sec"
    elif delta["days"] == 0:
      fmt = "{hrs} hr(s) {min} min {sec} sec"
    else:
      fmt = "{days} day(s) {hrs} hr(s) {min} min {sec} sec"
    return fmt.format(**delta)
