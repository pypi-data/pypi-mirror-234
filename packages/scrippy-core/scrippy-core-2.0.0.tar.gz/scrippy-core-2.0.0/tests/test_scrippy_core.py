#!/usr/bin/python3
"""
--------------------------------------------------------------------------------
  @author         : Michaël Costa (michael.costa@mcos.nc)
  @date           : 04/02/2021
  @version        : 1.0.0
  @description    : Script de test

--------------------------------------------------------------------------------
  Mise a jour :
  1.0.0  04/02/2021 - Michaël Costa - Cre: Création

--------------------------------------------------------------------------------
  Liste des utilisateurs ou groupe autorisés:
    @user:root

--------------------------------------------------------------------------------
  Liste des paramètres de configuration obligatoires:
    <section>|<clef>|<type>|<secret>
    @conf:database|host|str
    @conf:database|port|int
    @conf:database|user|str|true
    @conf:database|password|str|true
    @conf:database|db|str
    @conf:git|host|str
    @conf:git|port|int
    @conf:git|user|str|true
    @conf:git|repo|str
    @conf:git|branch|str
    @conf:git|ssh_cmd|str
    @conf:smtp|host|str
    @conf:smtp|port|int
    @conf:pop|host|str
    @conf:pop|port|int
    @conf:pop|user|str|true
    @conf:pop|password|str|true
    @conf:ssh|host|str
    @conf:ssh|port|int
    @conf:ssh|user|str|true
    @conf:ssh|keyfile|str|true
    @conf:api|host|str
    @conf:api|port|int
    @conf:api|endpoint|str


--------------------------------------------------------------------------------
  Liste des paramètres des options et arguments d'exécution:
    <nom>|<type>|<help>|<num_args>|<defaut>|<conflit>|<implique>|<requis>|<secret>
    @args:remote_path|str|Chemin distant|1||||true|false
    @args:remote_filename|str|nom du fichier distant|1||||true|false
    @args:local_path|str|Chemin local|1||||true|false
    @args:pattern|str|Motif|1|.*|||false|false
    @args:mail_recipient|choice|Adresse de courriel du destinataire|1|harry.fink@flying.circus,luiggi,vercotti@flying.circus|||true|true


--------------------------------------------------------------------------------
  Fonctionnement:
  ---------------
    Script de test du cadriciel Scrippy.

    Ce script exploite un panel des fonctionnalités proposées par le cadriciel Scrippy telles que:
    - Exploitation d'API
    - Manipulation de base de données
    - Envoi (SMTP) et reception (POP3) de courriel
    - Exécution de commandes distantes (SSH)
    - Transfert de fichiers (SFTP)
    - Manipulation de dépôts Git
    - Manipulation de fichiers modèles (Template Jinja2)

  D'autres fonctionnalités sont disponibles: https://codeberg.org/scrippy
"""
# --------------------------------------------------------------------------
#  Initialisation de l’environnement
# --------------------------------------------------------------------------
import os
import json
import email
import shutil
import scrippy_core
from scrippy_core import logger
from scrippy_db.db import Db
from scrippy_git.git import Repo
from scrippy_remote.remote import Ssh
from scrippy_api.api.client import Client
from scrippy_template.template import Renderer
from scrippy_mail.mail import Mailer, PopClient


# --------------------------------------------------------------------------
#  fonctions
# --------------------------------------------------------------------------
def get_api_user_list(host, port, endpoint):
  """Récupère la liste des utilisateurs à partir de l'API."""
  logger.info("[+] Récupération de la liste des utilisateurs depuis l'API")
  params = {}
  url = f"http://{host}:{port}/{endpoint}"
  client = Client(verify=False)
  response = client.request(method="GET", url=url, params=params)
  assert response.status_code == 200
  users = response.json()['users']
  for user in users:
    logger.info(f" '-> First name: {user['first_name']} / Last name: {user['last_name']} / Password: {user['password']}")
  return response.json()


def add_api_user(host, port, endpoint, user):
  """Ajoute un utilisateur à l'aide de l'API."""
  logger.info("[+] Ajout de l'utilisateur à l'aide de l'API")
  for attr in user["user"]:
    logger.info(f" '-> {attr}: {user['user'][attr]}")
  url = f"http://{host}:{port}/{endpoint}"
  client = Client(verify=False)
  response = client.request(method="PUT", url=url, data=json.dumps(user))
  assert response.status_code == 200
  return response.json()


def get_db_users(username, host, port, database, password):
  """Récupère la liste des utilisateurs à partir de la base de données."""
  logger.info("[+] Récupération de la liste des utilisateurs depuis la base de données")
  with Db(username=username, host=host, port=port, database=database, password=password) as db:
    req = "select id, name, givenname, password from users order by id;"
    params = None
    users = db.execute(req, params)
    for user in users:
      logger.info(f" '-> ID: {user[0]} / Last name: {user[1]} / First name: { user[2]} / Password: {user[3]}")
    return users


def add_db_user(username, host, port, database, password, user):
  """Ajout une utilisateur dans la base de données."""
  logger.info("[+] Ajout d'un utilisateur dans la base de données")
  for attr in user:
    logger.info(f" '-> {attr}")
  with Db(username=username, host=host, port=port, database=database, password=password) as db:
    req = "insert into users values (DEFAULT, %s, %s, %s) returning id;"
    params = user
    result = db.execute(req, params=params, commit=True)
    logger.info(result)
    return result


def render_template(template, params):
  """Rendu de fichiers modèles."""
  logger.info("[+] rendu du fichier modèle")
  logger.info(f" '-> {template}")
  base_path = scrippy_core.env.get("templatedir")
  renderer = Renderer(base_path, template)
  return renderer.render(params=params)


def send_mail(host, port, rcpt, body):
  """Envoi d'un courriel."""
  logger.info("[+] Envoi du courriel")
  mailer = Mailer(host=host, port=port, starttls=False)
  mail_from = "luiggi.vercotti@flying.circus"
  mail_to = (rcpt, )
  mail_subject = "Nobody expects the spanish inquisition"
  mail_body = body
  return mailer.send(mail_subject, mail_body, mail_to, mail_from)


def get_mail(host, port, username, password):
  """Récupération d'un courriel."""
  logger.info("[+] Récupération du courriel")
  pop_client = PopClient(host=host, port=port)
  pop_client.connect()
  pop_client.authenticate(username, password)
  num_available_mails = pop_client.stat().decode()[4]
  logger.info(f" '-> Nombre de courriels disponibles: {num_available_mails}")
  assert num_available_mails == "1"
  logger.info("  '-> Ok")
  mail_content = pop_client.retr(1)
  mail_content = email.message_from_bytes(mail_content).get_payload()
  mail_content = mail_content.replace("=\r\n", "")
  mail_content = mail_content.replace("\r\n.\r\n", "\n")
  mail_content = "\n".join(mail_content.split("\r\n"))
  logger.info(f" '-> {mail_content}")
  return mail_content


def delete_mail(host, port, username, password, num):
  """Suppression des courriels."""
  logger.info("[+] Suppression des courriels")
  pop_client = PopClient(host=host, port=port)
  pop_client.connect()
  pop_client.authenticate(username, password)
  return pop_client.dele(num)


def git_clone(repo, branch, path, env):
  """Clonage de dépôt Git."""
  logger.info("[+] Clonage du dépôt:")
  repo.clone(branch=branch, path=path, env=env)


def git_push(repo, message):
  """Pousse les modifications vers le dépôt distant."""
  logger.info("[+] Envoi des modifications")
  repo.commit_push(message)


def ssh_send_files(username, hostname, port, key_filename, local_path, remote_path, pattern):
  """Envoi de fichiers sur hôte distant."""
  logger.info("[+] Envoi des fichiers via SSH")
  with Ssh(username=username, hostname=hostname, port=port, key_filename=key_filename) as remote_host:
    local_files = remote_host.find_local_files(local_path, pattern, recursive=True)
    err = remote_host.transfer_local_files(local_files, remote_path, exit_on_error=True)
    err += remote_host.delete_local_files(local_files, exit_on_error=True)
    return err


def ssh_exec_cmd(username, hostname, port, key_filename, cmd):
  """Exécution d'une commande sur hôte distant."""
  logger.info("[+] Exécution de la commande sur l'hôte distant")
  logger.info(f" '-> {cmd}")
  with Ssh(username=username, hostname=hostname, port=port, key_filename=key_filename) as remote_host:
    return remote_host.exec_command(cmd, return_stdout=True)


def ssh_get_file(username, hostname, port, key_filename, local_path, remote_path, remote_filename):
  """Récupération de fichier depuis l'hôte distant."""
  pattern = os.path.join(remote_path, remote_filename)
  logger.info("[+] Récupération du fichier distant")
  logger.info(f" '-> {pattern}")
  with Ssh(username=username, hostname=hostname, port=port, key_filename=key_filename) as remote_host:
    remote_files = remote_host.find_remote_files(remote_path, pattern, recursive=True, exit_on_error=True)
    err = remote_host.transfer_remote_files(local_path, remote_files, exit_on_error=True)
    err += remote_host.delete_remote_files(remote_files, exit_on_error=True)
    return err


# --------------------------------------------------------------------------
#  Traitement principal
# --------------------------------------------------------------------------
def main():
  with scrippy_core.ScriptContext() as _context:
    config = _context.config
    args = _context.args
    logger.info("[+] Test started...")
    # --------------------------------------------------------------------------
    #  Test du client d'API
    # --------------------------------------------------------------------------
    new_user = {"user": {"first_name": "Harry", "last_name": "Fink", "password": "D3ADP4RR0T"}}
    expected = {"user": new_user["user"], "method": "PUT"}
    result = add_api_user(config.get("api", "host"), config.get("api", "port"), config.get("api", "endpoint"), new_user)
    assert result == expected
    result = get_api_user_list(config.get("api", "host"), config.get("api", "port"), config.get("api", "endpoint"))
    assert len(result["users"]) == 11
    assert new_user["user"] in result["users"]
    # --------------------------------------------------------------------------
    #  Test du client Base de données
    # --------------------------------------------------------------------------
    user = ("VERCOTTI", "Luiggi", "SP4N15H1NQU1S1T10N")
    result = add_db_user(config.get("database", "user"),
                         config.get("database", "host"),
                         config.get("database", "port", "int"),
                         config.get("database", "db"),
                         config.get("database", "password"),
                         user)
    assert result[0][0] == 1
    users = get_db_users(config.get("database", "user"),
                         config.get("database", "host"),
                         config.get("database", "port", "int"),
                         config.get("database", "db"),
                         config.get("database", "password"))
    assert len(users) == 2 and users[0][1] == "FINK" and users[0][2] == "Harry"
    assert users[1][0] == 1, users[1][1] == "VERCOTTI" and users[1][2] == "Luiggi"
    # --------------------------------------------------------------------------
    #  Test du moteur de modèles
    # --------------------------------------------------------------------------
    params = {"user": {"first_name": users[0][2],
                       "last_name": users[0][1],
                       "password": users[0][3]},
              "sender": {"first_name": users[1][2],
                         "last_name": users[1][1]}}
    mail_body = render_template(template=config.get("templates", "filename"), params=params)
    logger.info(mail_body)
    with open(os.path.join(scrippy_core.env.get("tmpdir"),
              "message.txt"),
              mode="w",
              encoding="utf-8") as message:
      message.write(mail_body)
    # --------------------------------------------------------------------------
    #  Test du client SMTP
    # --------------------------------------------------------------------------
    assert send_mail(host=config.get("smtp", "host"),
                     port=config.get("smtp", "port", "int"),
                     rcpt=args.mail_recipient,
                     body=mail_body)
    # --------------------------------------------------------------------------
    #  Test du client POP3
    # --------------------------------------------------------------------------
    mail_content = get_mail(host=config.get("pop", "host"),
                            port=config.get("pop", "port", "int"),
                            username=config.get("pop", "user"),
                            password=config.get("pop", "password"))
    assert mail_content.strip() == mail_body.strip()
    dele_result = delete_mail(host=config.get("pop", "host"),
                              port=config.get("pop", "port", "int"),
                              username=config.get("pop", "user"),
                              password=config.get("pop", "password"),
                              num=1)
    logger.info(dele_result)
    assert dele_result.decode()[:3] == "+OK"
    # --------------------------------------------------------------------------
    #  Test du client Git
    # --------------------------------------------------------------------------
    ssh_cmd = config.get("git", "ssh_cmd").format(os.path.dirname(os.path.realpath(__file__)))
    local_path = os.path.join(scrippy_core.env.get("tmpdir"),
                              config.get("git", "repo"))
    ENV = {"GIT_SSH_VARIANT": "ssh",
           "GIT_SSH_COMMAND": ssh_cmd}
    repo = Repo(username=config.get("git", "user"),
                host=config.get("git", "host"),
                port=config.get("git", "port", "int"),
                reponame=config.get("git", "repo"))
    git_clone(repo, branch=config.get("git", "branch"), path=local_path, env=ENV)
    shutil.copy(os.path.join(scrippy_core.env.get("tmpdir"),
                             "message.txt"),
                os.path.join(local_path, "message.txt"))
    git_push(repo, "Harry fink is a new user")
    # --------------------------------------------------------------------------
    #  Test du client SSH
    # --------------------------------------------------------------------------
    key_filename = config.get("ssh", "keyfile").format(os.path.dirname(os.path.realpath(__file__)))
    err = ssh_send_files(username=config.get("ssh", "user"),
                         hostname=config.get("ssh", "host"),
                         port=config.get("ssh", "port", "int"),
                         key_filename=key_filename,
                         local_path=args.local_path,
                         remote_path=args.remote_path,
                         pattern=args.pattern)
    assert err == 0
    cmd = f"find {args.remote_path} -type f"
    stdout = ssh_exec_cmd(username=config.get("ssh", "user"),
                          hostname=config.get("ssh", "host"),
                          port=config.get("ssh", "port", "int"),
                          key_filename=key_filename,
                          cmd=cmd)
    assert stdout["exit_code"] == 0
    err = ssh_get_file(username=config.get("ssh", "user"),
                       hostname=config.get("ssh", "host"),
                       port=config.get("ssh", "port", "int"),
                       key_filename=key_filename,
                       local_path=os.path.dirname(args.local_path),
                       remote_path=args.remote_path,
                       remote_filename=args.remote_filename)
    assert err == 0
    assert os.path.isfile(os.path.join(os.path.dirname(args.local_path), args.remote_filename))

    # --------------------------------------------------------------------------
    logger.info("[+] Test finished !")


# --------------------------------------------------------------------------
#  Point d'entrée
# --------------------------------------------------------------------------
if __name__ == '__main__':
  main()
