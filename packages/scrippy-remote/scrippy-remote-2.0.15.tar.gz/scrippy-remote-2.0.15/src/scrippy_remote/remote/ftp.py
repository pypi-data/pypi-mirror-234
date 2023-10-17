"""The scrippy_remote.remote.ftp module implements the client part of the FTP protocol in the form of the Ftp class."""
import os
import re
import ssl
from scrippy_remote.remote.scrippy_ftp import FtpSimple, Ftps, Ftpes
from scrippy_remote import ScrippyRemoteError, logger


class Ftp:
  """
  The main class for manipulating remote hosts via FTP.
  """

  def __init__(self, hostname, port=21,
               username="anonymous", password="",
               tls=True, explicit=True, ssl_verify=True,
               ssl_version=ssl.PROTOCOL_TLSv1_2):
    logger.debug("[+] Connection initialization:")
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    self.tls = tls
    self.explicit = explicit
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl_version
    if self.tls:
      if explicit:
        self.remote = Ftpes(self.hostname,
                            self.port,
                            self.username,
                            self.password,
                            self.ssl_verify,
                            self.ssl_version)
      else:
        self.remote = Ftps(self.hostname,
                           self.port,
                           self.username,
                           self.password,
                           self.ssl_verify,
                           self.ssl_version)
    else:
      self.remote = FtpSimple(self.hostname,
                              self.port,
                              self.username,
                              self.password)

  def __enter__(self):
    """Entry point."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Exit point."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """Connect to remote FTP server."""
    connected = False
    logger.debug(f"[+] Connecting to {self.username}@{self.hostname}:{self.port}")
    try:
      connected = self.remote.connect()
      if connected:
        self.remote.login()
    except Exception as err:
      logger.critical(f" +-> Unexpected error: [{err.__class__.__name__}] {err}")
    finally:
      return connected

  def close(self):
    """Ferme la connexion."""
    logger.debug(f"[+] Closing connection to {self.username}@{self.hostname}")
    if self.remote:
      self.remote.close()

  def get_file(self, remote_file, local_dir, create_dir=False):
    """
    Retrieve the remote file 'filepath' and copy it to 'local_dir'.
    If 'create_dir' is set to True, then the remote directory structure is recreated locally in the 'local_dir' directory.

    Example:

    get_file(remote_file='/dead/parrot/parrot.txt',
             local_dir='/home/luiggi.vercotti',
             create_dir=True)

    will create the local directory structure: '/home/luiggi.vercotti/dead/parrot' and copy the remote file '/dead/parrot/parrot.txt' to it as
    '/home/luiggi.vercotti/dead/parrot/parrot.txt'.
    """
    local_fname = os.path.join(local_dir, remote_file)
    if create_dir:
      self.create_local_dirs(remote_file, local_dir)
    logger.debug(f"[+] Downloading file: {remote_file}")
    logger.debug(f" '-> {local_fname}")
    try:
      self.remote.retrbinary(f"RETR {remote_file}",
                             open(local_fname, 'wb').write)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err

  def put_file(self, local_file, remote_dir='/', create_dir=False):
    """
    Upload the local file 'local_file' to the remote server in the 'remote_dir' directory.
    If 'create_dir' is set to True, the directory structure in 'remote_dir' will be created on the remote server.

    Example:

    put_file(local_file='/home/luiggi.vercotti/dead/parrot/parrot.txt',
             remote_dir='/spanish/inquisition',
             create_dir=True)

    will create the remote directory structure: '/spanish/inquisition'
    and place the remote file: '/spanish/inquisition/parrot.txt'
    """
    if remote_dir[0] == "/":
      remote_dir = remote_dir[1:]
    remote_file = os.path.basename(local_file)
    remote_fname = os.path.join(remote_dir, remote_file)
    if create_dir:
      self.create_remote_dirs(remote_dir=remote_dir)
      remote_fname = os.path.join(remote_dir, remote_file)
    logger.debug(f"[+] Uploading file: {remote_file}")
    logger.debug(f" '-> {remote_fname}")
    try:
      self.remote.storbinary(f"STOR {remote_fname}", open(local_file, "rb"))
    except Exception as err:
      err_msg = f"Error while transferring file: [{err.__class__.__name__}]: {err}"
      logger.critical(err_msg)
      raise ScrippyRemoteError(err_msg) from err

  def create_local_dirs(self, remote_file, local_dir):
    """
    Create the directory structure of 'remote_file' in the 'local_dir' directory.     The last component of 'remote_file' is treated as a file.

    Example:

    create_local_dirs('/dead/parrot/dead_parrot.txt', '/home/luiggi.vercotti')

    will create the local directory structure: '/home/luiggi.vercotti/dead/parrot/'.
    """
    hierarchy = os.path.join(*remote_file.split('/')[:-1])
    hierarchy = os.path.join(local_dir, hierarchy)
    logger.debug("[+] Local file hierarchy creation:")
    logger.debug(f" '-> {hierarchy}")
    try:
      os.makedirs(hierarchy, exist_ok=True)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err

  def create_remote_dirs(self, remote_dir):
    """
    Create the directory structure 'remote_dirs' on the remote host.
    """
    hierarchy = remote_dir.split('/')
    logger.debug("[+] Remote file hierarchy creation:")
    r_dir = ""
    for component in hierarchy:
      r_dir = os.path.join(r_dir, component)
      logger.debug(f" '-> {r_dir}")
      try:
        self.remote.mkd(r_dir)
      except Exception as err:
        err_msg = f"[{err.__class__.__name__}] {err}"
        logger.critical(f" '-> {err_msg}")
        raise ScrippyRemoteError(err_msg) from err

  def delete_remote_file(self, remote_file):
    """
    Delete the remote file specified by the full path passed as an argument.
    """
    try:
      self.remote.delete(remote_file)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err

  def delete_remote_dir(self, remote_dir):
    """
    Delete the remote directory specified by the full path passed as an argument.
    """
    try:
      self.remote.rmd(remote_dir)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err

  def list(self, remote_dir, file_type='f', pattern='.*'):
    """
    Returns the list of files in the remote directory 'remote_dir'.

    The 'file_type' argument allows to select the type of files listed (f=file (default value), d=directory).
    """
    content = []
    logger.debug(f"[+] Getting remote content from folder: {remote_dir}")
    try:
      self.remote.retrlines(f"LIST {remote_dir}", content.append)
      if file_type == 'f':
        reg = re.compile("^-.*")
      elif file_type == 'd':
        reg = re.compile("^d.*")
      content = [os.path.join(remote_dir, f.split()[-1]) for f in content if re.match(reg, f)]
      reg = re.compile(pattern)
      return [f.split()[-1] for f in content if re.match(reg, f)]
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err
