"""The scrippy_remote.remote.ssh module implements the client part of the SSH/SFTP protocol in the form of the Ssh class."""
import os
import re
import stat
import socket
import logging
import paramiko
from time import sleep
from scrippy_remote import ScrippyRemoteError, logger


def clean_path(path):
  """
  Removes any trailing slashes from the path.

  :param path: path to clean
  :return: returns path without trailing '/' if present"
  """
  if path[-1:] == "/":
    path = path[:-1]
  return path


def _log_line(line, log_content, log_level):
  if log_content:
    logger.log(log_level, f" '-> {line}")


class Ssh:
  """
  The main class for manipulating remote hosts via SSH.

  This class allows:
  - Remote command execution
  - File transfer
  """

  def __init__(self, username, hostname, port=22,
               password=None, key_filename=None):
    if logger.level != logging.DEBUG:
      logging.getLogger("paramiko").setLevel(logging.ERROR)
    self.username = username
    self.hostname = hostname
    self.port = port
    self.key_filename = key_filename
    self.password = password
    self.remote = None

  def __enter__(self):
    """Entry point."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Exit point."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """
    Connects to a remote host.

    The ~/.ssh directory of the current user is searched to find the appropriate SSH key.

    An error is raised, and False is returned in at least the following cases:

    - The key for the remote host is not found in the ~/.ssh/known_hosts file of the current user.
    - The key for the remote host differs from the one recorded in the ~/.ssh/known_hosts file of the current user.
    - User authentication failed.
    - The remote host is unreachable/unknown.
    - The SSH key was not found.
    - ...
    """
    logger.debug(f"[+] Connecting to {self.username}@{self.hostname}:{self.port}")
    try:
      self.remote = paramiko.SSHClient()
      self.remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      self.remote.load_system_host_keys()
      if self.key_filename:
        logger.debug(f"Using key: {self.key_filename}")
        pkey = paramiko.RSAKey.from_private_key_file(self.key_filename, password=self.password)
        logger.debug("Connection")
        self.remote.connect(hostname=self.hostname,
                            port=self.port,
                            username=self.username,
                            pkey=pkey)
      elif self.password:
        logger.debug(f"Using password: {self.password}")
        self.remote.connect(hostname=self.hostname,
                            port=self.port,
                            username=self.username,
                            password=self.password,
                            allow_agent=False,
                            look_for_keys=False)
      else:
        logger.debug("Using default SSH key")
        self.remote.connect(hostname=self.hostname,
                            port=self.port,
                            username=self.username)
    except paramiko.BadHostKeyException as err:
      err_msg = f"Bad SSH Host Key : [{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err
    except paramiko.AuthenticationException as err:
      err_msg = f"Failed to authenticate: [{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err
    except (paramiko.SSHException,
            socket.gaierror,
            paramiko.ssh_exception.NoValidConnectionsError,
            FileNotFoundError) as err:
      err_msg = f"Connection error: [{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err
    except Exception as err:
      err_msg = f"Unexpected error: [{err.__class__.__name__}] {err}"
      logger.critical(f" +-> {err_msg}")
      raise ScrippyRemoteError(err_msg) from err

  def close(self):
    """Close connection to remote host."""
    logger.debug(f"[+] Closing connection to {self.username}@{self.hostname}")
    if self.remote:
      self.remote.close()

  def exec_command(self, command, return_stdout=False, log_stdout=True, log_stderr=True, strip_stdout=True, strip_stderr=True, **kwargs):
    """
    Execute a command on the remote host and returns the exit_code.

    This method accepts all the arguments from http://docs.paramiko.org/en/stable/api/client.html#paramiko.client.SSHClient.exec_command

    :param bool return_stdout: add a list of stdout lines in the returned dict (default False).
    :param bool log_stdout: log stdout in logging Info (default True).
    :param bool log_stderr: log stderr in logging Error (default True).
    :param bool strip_stdout: remove white characters (spaces, tabs, etc.) from each line of the standard output returned by the command (default True).
    :param bool strip_stderr: remove white characters (spaces, tabs, etc.) from each line of the standard error returned by the command (default True)."

    :return:
        a dict containing ``exit_code`` of the executing command (ex: ``{ "exit_code": 0 }``)
        if return_stdout == True add a key ``stdout`` containing stdout lines as a list of line

    :raises: `SystemExit` -- if the server fails to execute the command
    """
    logger.debug(f"[+] Running command: {command}")
    try:
      exit_code = None
      stdin, stdout, stderr = self.remote.exec_command(command, **kwargs)
      channel = stdout.channel
      stdout_content = []
      while True:
        sleep(0.1)
        while channel.recv_ready():
          line = stdout.readline()
          if strip_stdout:
            line = line.strip()
          _log_line(line, log_stdout, logging.DEBUG)
          if return_stdout:
            stdout_content.append(line)
        while channel.recv_stderr_ready():
          line = stderr.readline()
          if strip_stderr:
            line = line.strip()
          _log_line(line, log_stderr, logging.ERROR)
        if channel.exit_status_ready():
          logger.debug(" '-> exit_status_ready !")
          # Read last lines
          for line in stdout:
            if strip_stdout:
              line = line.strip()
            _log_line(line, log_stdout, logging.DEBUG)
            if return_stdout:
              stdout_content.append(line)
          for line in stderr:
            if strip_stderr:
              line = line.strip()
            _log_line(line, log_stderr, logging.ERROR)
          exit_code = channel.recv_exit_status()
          break
      res = {'exit_code': exit_code}
      if return_stdout:
        res['stdout'] = stdout_content
      return res
    except paramiko.SSHException as err:
      err_msg = f"Error while running command: [{err.__class__.__name__}] {err}"
      logger.critical(err_msg)
      raise ScrippyRemoteError(err_msg) from err

# -- OPEN ----------------------------------------------------------------------

  def open_for_read(self, file):
    sftp = self.remote.open_sftp()
    return sftp.open(file, mode='r')

  def open_for_write(self, file):
    sftp = self.remote.open_sftp()
    return sftp.open(file, mode='w')

# -- PUT -----------------------------------------------------------------------

  def sftp_put(self, local_path, remote_path, pattern='.*', recursive=True, delete=False, exit_on_error=True):
    """
    Send files to the remote host.

    local_path and remote_path must be directories.

    The pattern parameter allows you to define a pattern to search for in file names. The pattern is searched in the file name only.

    If recursive is set to True (default=True), then the pattern defined by the pattern parameter is searched in all file names contained in the directory defined by local_path. Files whose names match the pattern are then transferred to the directory defined by remote_path.

    If delete is set to True (default=False), local files will be deleted once all files have been transferred to the remote host.

    If an error is raised during the transfer, local files are not deleted, even if exit_on_error is set to False.

    If the optional exit_on_error parameter is set to True (default=True):
    - The transfer is interrupted at the first error.
    - The deletion of local files is interrupted at the first error.
    - The function returns the number of errors encountered during batch processing.

    Otherwise (exit_on_error=False):
    - The error is logged, but batch processing is not interrupted.
    - The function returns the number of errors encountered during batch processing.
    """
    local_path = clean_path(local_path)
    remote_path = clean_path(remote_path)
    num_err = 0
    try:
      files = self.find_local_files(local_path, pattern, recursive)
      num_err = self.transfer_local_files(files, remote_path, exit_on_error)
      if num_err == 0 and delete:
        self.delete_local_files(files, exit_on_error)
      elif delete:
        logger.error(f"[+] Encountered errors: {num_err}")
        logger.error(" '-> File deletion aborted")
      return num_err
    except Exception as err:
      msg = "Unrecoverable error"
      if exit_on_error:
        msg = "exit_on_error is set to True"
      logger.error(f"[{err.__class__.__name__}] {err}: Stopping execution")
      logger.error(f" '-> {msg}: Stopping execution")
      if num_err == 0:
        num_err += 1
      return num_err

  def find_local_files(self, local_path, pattern, recursive):
    logger.debug("[+] Getting local files list")
    logger.debug(f" '-> Local folder: {local_path}")
    logger.debug(f" '-> Pattern: {pattern}")
    regex = re.compile(pattern)
    local_files = []
    local_dirs = []
    for fname in os.listdir(local_path):
      fname = os.path.join(local_path, fname)
      if os.path.isdir(fname):
        local_dirs.append(fname)
      else:
        if regex.match(fname) is not None:
          logger.debug(f" '-> {fname}")
          local_files.append(fname)
    if recursive:
      for ldir in local_dirs:
        local_files += self.find_local_files(ldir, pattern, recursive)
    return local_files

  def transfer_local_files(self, local_files, remote_path, exit_on_error):
    num_err = 0
    sftp = self.remote.open_sftp()
    logger.debug(f"[+] File transfert to {self.username}@{self.hostname}:{self.port}:{remote_path}")
    if len(local_files) == 0:
      logger.debug(" '-> No file found")
    for local_file in local_files:
      logger.debug(f" '-> {local_file}")
      remote_fname = os.path.join(remote_path, os.path.basename(local_file))
      try:
        sftp.put(local_file, remote_fname, confirm=True)
      except Exception as err:
        num_err += 1
        logger.warning(f"  '-> [{err.__class__.__name__}] {err}")
        if exit_on_error:
          err_msg = "Transfert error and exit_on_error is set to True: Immediate abortion."
          logger.critical(err_msg)
          raise ScrippyRemoteError(err_msg) from err
    return num_err

  def delete_local_files(self, local_files, exit_on_error):
    num_err = 0
    logger.debug("[+] Local files deletion")
    if len(local_files) == 0:
      logger.debug(" '-> No file found")
    for local_file in local_files:
      logger.debug(f" '-> {local_file}")
      try:
        os.remove(local_file)
      except Exception as err:
        num_err += 1
        logger.warning(f"  '-> [{err.__class__.__name__}] {err}")
        if exit_on_error:
          err_msg = "Error while deleting and exit_on_error is set to True: Immediate abortion."
          logger.critical(err_msg)
          raise ScrippyRemoteError(err_msg) from err
    return num_err

# -- GET -----------------------------------------------------------------------
  def sftp_get(self, remote_path, local_path, pattern='.*', recursive=True, delete=False, exit_on_error=True):
    """
    Retrieve files from the remote host.
    local_path and remote_path must be directories.

    The pattern parameter allows you to define a pattern to search for in file names. The pattern is searched in the file name only.

    If recursive is set to True (default=True), then the pattern defined by the pattern parameter is searched in all file names contained in the directory defined by remote_path. Files whose names match the pattern are then transferred to the directory defined by local_path.

    If delete is set to True (default=False), remote files will be deleted once all files have been transferred to the local host.

    If a transfer error is raised during the transfer, local files are not deleted, even if exit_on_error is set to False.

    If the optional exit_on_error parameter is set to True (default=True):

    - The transfer is interrupted at the first error.
    - The deletion of remote files is interrupted at the first error.
    - The function returns the number of errors encountered during batch processing.

    Otherwise (exit_on_error=False):
    - The error is logged, but batch processing is not interrupted.
    - The function returns the number of errors encountered during batch processing.
    """
    err = 0
    local_path = clean_path(local_path)
    remote_path = clean_path(remote_path)
    remote_files = self.find_remote_files(remote_path,
                                          pattern,
                                          recursive,
                                          exit_on_error)
    err += self.transfer_remote_files(local_path,
                                      remote_files,
                                      exit_on_error)
    if delete and err == 0:
      err += self.delete_remote_files(remote_files, exit_on_error)
    elif delete:
      logger.error(f"[+] Encountered errors: {err}")
      logger.error(" '-> File deletion aborted")
    return err

  def find_remote_files(self, remote_path, pattern, recursive, exit_on_error, sftp=None):
    if sftp is None:
      sftp = self.remote.open_sftp()

    logger.debug("[+] Getting remote files list")
    logger.debug(f" '-> Remote folder: {remote_path}")
    logger.debug(f" '-> Pattern: {pattern}")
    regex = re.compile(pattern)
    remote_files = []
    remote_dirs = []
    try:
      for f in sftp.listdir_attr(remote_path):
        fname = os.path.join(remote_path, f.filename)
        if stat.S_ISDIR(f.st_mode):
          remote_dirs.append(fname)
        else:
          if regex.match(fname) is not None:
            logger.debug(f" '-> {fname}")
            remote_files.append(fname)
      if recursive:
        for directory in remote_dirs:
          remote_files += self.find_remote_files(directory, pattern, recursive, exit_on_error, sftp)
    except Exception as err:
      err_msg = f"Error while getting file list: [{err.__class__.__name__}] {err}"
      logger.warning(err_msg)
      if exit_on_error:
        err_msg = "Error while getting file list and exit_on_error set to True: Immediate abortion."
        logger.critical(err_msg)
        raise ScrippyRemoteError(err_msg) from err
    return remote_files

  def transfer_remote_files(self, local_path, remote_files, exit_on_error):
    num_err = 0
    sftp = self.remote.open_sftp()
    logger.debug(f"[+] File transfert from {self.username}@{self.hostname}:{self.port}")
    if len(remote_files) == 0:
      logger.debug(" '-> No file found")
    for remote_file in remote_files:
      local_fname = os.path.basename(remote_file)
      local_fname = os.path.join(local_path, local_fname)
      logger.debug(f" '-> {remote_file}")
      logger.debug(f" '-> {local_fname}")
      try:
        sftp.get(remote_file, local_fname)
      except Exception as err:
        num_err += 1
        err_msg = f"[{err.__class__.__name__}] {err}"
        logger.warning(err_msg)
        if exit_on_error:
          err_msg = "Error while transfering and exit_on_error set to True: Immediate abortion."
          logger.critical(err_msg)
          raise ScrippyRemoteError(err_msg) from err
    return num_err

  def delete_remote_files(self, remote_files, exit_on_error):
    num_err = 0
    sftp = self.remote.open_sftp()
    logger.debug("[+] Remote files deletion")
    if len(remote_files) == 0:
      logger.debug(" '-> No file found")
    for remote_file in remote_files:
      try:
        logger.debug(f" '-> {remote_file}")
        sftp.remove(remote_file)
      except Exception as err:
        num_err += 1
        err_msg = f"[{err.__class__.__name__}] {err}"
        logger.warning(err_msg)
        if exit_on_error:
          err_msg = "Error while deleting and exit_on_error set to True: Immediate abortion."
          logger.critical(err_msg)
          raise ScrippyRemoteError(err_msg) from err
    return num_err

# -- DELETE --------------------------------------------------------------------
  def sftp_delete(self, remote_path, pattern, recursive, exit_on_error):
    remote_files = self.find_remote_files(remote_path,
                                          pattern,
                                          recursive,
                                          exit_on_error)
    return self.delete_remote_files(remote_files, exit_on_error)

# -- LIST ----------------------------------------------------------------------
  def sftp_list(self, remote_path, pattern, recursive, exit_on_error):
    return self.find_remote_files(remote_path,
                                  pattern,
                                  recursive,
                                  exit_on_error)

# -- STAT ----------------------------------------------------------------------
  def sftp_stat(self, remote_path, pattern, recursive, exit_on_error):
    """
    Returns a dict {'file_path': stat}
    See http://docs.paramiko.org/en/stable/api/sftp.html#paramiko.sftp_client.SFTPClient.stat
    """
    remote_files_stats = {}
    remote_files = self.sftp_list(remote_path,
                                  pattern,
                                  recursive,
                                  exit_on_error)
    sftp = self.remote.open_sftp()
    for file_name in remote_files:
      file_stat = sftp.stat(file_name)
      remote_files_stats[file_name] = file_stat
    return remote_files_stats

  def sftp_file_exist(self, remote_filename):
    sftp = self.remote.open_sftp()
    try:
      if stat.S_ISDIR(sftp.stat(remote_filename).st_mode):
        raise ScrippyRemoteError(f"{remote_filename} exists and is a directory")
      return True
    except IOError:
      return False

# -- UTIL ----------------------------------------------------------------------
  def sftp_mkdir_p(self, remote_path):
    """
    Create the directory tree on the remote host corresponding to remote_path. This method is recursive and, in addition to the path to create, requires the sftp connection as an argument.
    """
    sftp = self.remote.open_sftp()
    if remote_path == '':
      remote_path = './'
    try:
      sftp.chdir(remote_path)
    except IOError:
      dirname, basename = os.path.split(remote_path.rstrip('/'))
      self.sftp_mkdir_p(dirname)
      sftp.mkdir(basename)
      sftp.chdir(basename)
    except Exception as err:
      err_msg = f"[{err.__class__.__name__}] {err}"
      logger.error(err_msg)
      raise ScrippyRemoteError(err_msg) from err
    return True
