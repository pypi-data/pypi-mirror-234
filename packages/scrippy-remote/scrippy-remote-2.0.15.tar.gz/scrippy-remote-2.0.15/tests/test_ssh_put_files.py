"""Module de test scrippy_remote.remote.Ssh."""
import os
from scrippy_remote.remote import Ssh
from scrippy_remote import ScrippyRemoteError, logger

remote_host = "sshd"
remote_port = 2200
remote_user = "scrippy"
remote_path = "/home/scrippy"
key_filename = f"{os.path.dirname(os.path.realpath(__file__))}/ssh/scrippy.rsa"
local_path = "/tmp"
test_filename = "parrot.txt"
pattern = f".*{test_filename}"


def test_put_file():
  """Test d'envoi de fichier."""
  recursive = False
  delete = False
  exit_on_error = True
  l_path = f"{os.path.dirname(os.path.realpath(__file__))}"
  with Ssh(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           key_filename=key_filename) as host:
    try:
      num_err = host.sftp_put(remote_path=remote_path,
                              local_path=l_path,
                              pattern=pattern,
                              recursive=recursive,
                              delete=delete,
                              exit_on_error=exit_on_error)
      logger.debug(f"Errors: {num_err}")
    except ScrippyRemoteError as err:
      logger.critical(f"{err}")
