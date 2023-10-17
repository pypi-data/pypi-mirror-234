"""Module de test scrippy_remote.remote.Ftp."""
import os
import hashlib
from scrippy_remote import logger
from scrippy_remote.remote.cifs import Cifs


local_file = f"{os.path.dirname(os.path.realpath(__file__))}/parrot.txt"
md5_local_file = hashlib.md5(open(local_file, "rb").read()).hexdigest()
remote_host = "samba"
remote_user = "luiggi.vercotti"
remote_password = "d34dp4rr0t"
remote_dir = "storage"
remote_user_dir = "luiggi.vercotti"
remote_file = f"{os.path.join(remote_user_dir, 'parrot.txt')}"
local_dir = "/tmp"


def test_put_file():
  """Test d'envoi de fichier."""
  with Cifs(username=remote_user,
            hostname=remote_host,
            shared_folder=remote_dir,
            password=remote_password) as cifs:
    cifs.create_directory(remote_user_dir)
    cifs.put_file(local_filepath=local_file,
                  remote_filepath=remote_file)


def test_get_remote_file():
  l_file = os.path.join(local_dir, 'parrot.txt')
  with Cifs(username=remote_user,
            hostname=remote_host,
            shared_folder=remote_dir,
            password=remote_password) as cifs:
    cifs.get_file(remote_filepath=remote_file,
                  local_filepath=l_file)
    assert os.path.isfile(l_file)
    logger.debug(f"MD5 local_file: {md5_local_file}")
    md5_l_file = hashlib.md5(open(l_file, "rb").read()).hexdigest()
    logger.debug(f"MD5 l_file: {md5_l_file}")
    assert md5_l_file == md5_local_file


def test_read_write_files():
  r_file = os.path.join(remote_user_dir, 'inquisition.txt')
  with Cifs(username=remote_user,
            hostname=remote_host,
            shared_folder=remote_dir,
            password=remote_password) as cifs:
    with cifs.open_for_write(r_file) as w_file:
      w_file.write(b'None expect the Spannish inquisition')
    with cifs.open_for_read(r_file) as rr_file:
      assert rr_file.readlines() == [b'None expect the Spannish inquisition']


def test_delete_remote_dir():
  with Cifs(username=remote_user,
            hostname=remote_host,
            shared_folder=remote_dir,
            password=remote_password) as cifs:
    cifs.delete_directory_content(remote_user_dir)
