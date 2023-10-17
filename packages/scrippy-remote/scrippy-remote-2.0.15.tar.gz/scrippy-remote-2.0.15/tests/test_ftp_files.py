"""Module de test scrippy_remote.remote.Ftp."""
import os
import hashlib
from scrippy_remote import logger
from scrippy_remote.remote import Ftp

remote_host = "vsftpd"
remote_port = 2990
remote_user = "luiggi.vercotti"
local_file = f"{os.path.dirname(os.path.realpath(__file__))}/parrot.txt"
md5_local_file = hashlib.md5(open(local_file, "rb").read()).hexdigest()
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
local_dir = "/tmp"
pattern = r".*\.txt"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False


def test_put_file():
  """Test d'envoi de fichier."""
  with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    host.put_file(local_file=local_file,
                  remote_dir=remote_dir,
                  create_dir=True)


def test_list_files():
  """Test de listing de répertoire."""
  with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    files = host.list(remote_dir=remote_dir,
                      pattern=pattern)
    assert f"{os.path.join(remote_dir, os.path.basename(local_file))}" in files


def test_get_remote_file():
  with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    remote_file = os.path.join(remote_dir, os.path.basename(local_file))
    host.get_file(remote_file=remote_file,
                  local_dir=local_dir,
                  create_dir=True)
    l_file = os.path.join(local_dir, remote_dir, os.path.basename(local_file))
    assert os.path.isfile(l_file)
    logger.debug(f"MD5 local_file: {md5_local_file}")
    md5_l_file = hashlib.md5(open(l_file, "rb").read()).hexdigest()
    logger.debug(f"MD5 l_file: {md5_l_file}")
    assert md5_l_file == md5_local_file


def test_delete_remote_file():
  with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    remote_file = os.path.join(remote_dir, os.path.basename(local_file))
    host.delete_remote_file(remote_file)
    files = host.list(remote_dir=remote_dir,
                      pattern=pattern)
    assert f"{os.path.join(remote_dir, os.path.basename(local_file))}" not in files


def test_delete_remote_dir():
  with Ftp(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           password=password,
           tls=ftp_tls,
           explicit=ftp_explicit_tls,
           ssl_verify=ftp_ssl_verify) as host:
    r_dir = os.path.dirname(remote_dir)
    host.delete_remote_dir(remote_dir)
    dirs = host.list(remote_dir=r_dir,
                     file_type="d",
                     pattern=".*")
    assert remote_dir not in dirs
