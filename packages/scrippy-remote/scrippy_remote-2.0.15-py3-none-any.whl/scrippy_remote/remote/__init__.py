"""
This module provides a comprehensive set of objects, methods, and functions for operations on remote hosts accessible via SSH/SFTP, FTP and CIFS/SMB.

  - Execution of commands on a remote host
  - Copying directories/files to a remote host
  - Deleting directories/files on a remote host
  - Copying files between remote hosts (with the local machine acting as a buffer)
    ...
"""

from scrippy_remote.remote.ssh import Ssh
from scrippy_remote.remote.ftp import Ftp
from scrippy_remote.remote.cifs import Cifs
