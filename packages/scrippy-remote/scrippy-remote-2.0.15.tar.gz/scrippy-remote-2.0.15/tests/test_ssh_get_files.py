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
test_filename = "inquisition.txt"
pattern = f".*{test_filename}"

good_files = [os.path.join(remote_path, test_filename)]
inexistant_files = ["/etc/inexistant"]
remote_dirs = ["/etc/ssh"]
remote_filenames = good_files + inexistant_files + remote_dirs


def test_get_file():
  """Test de récuperation de fichier."""
  recursive = False
  delete = False
  exit_on_error = True
  with Ssh(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           key_filename=key_filename) as host:
    try:
      num_err = host.sftp_get(remote_path=remote_path,
                              local_path=local_path,
                              pattern=pattern,
                              recursive=recursive,
                              delete=delete,
                              exit_on_error=exit_on_error)
      logger.debug(f"Errors: {num_err}")
      assert os.path.isfile(os.path.join(local_path, test_filename))
    except ScrippyRemoteError as err:
      logger.critical(f"{err}")


def test_file_exist():
  with Ssh(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           key_filename=key_filename) as host:
    for remote_filename in remote_filenames:
      try:
        if host.sftp_file_exist(remote_filename):
          assert remote_filename in good_files
        else:
          assert remote_filename in inexistant_files
      except ScrippyRemoteError as err:
        assert str(err).endswith("exists and is a directory")
        assert remote_filename in remote_dirs
