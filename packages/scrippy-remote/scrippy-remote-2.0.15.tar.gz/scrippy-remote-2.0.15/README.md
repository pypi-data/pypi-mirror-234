
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-remote/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-remote.png "Scrippy, my scrangourou friend")

# `scrippy_remote`

SSH/SFTP/FTP client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python modules

#### List of necessary modules

The modules listed below will be automatically installed.

- paramiko

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-remote.git
cd scrippy-remote
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-remote
```

### Usage

### `scrippy_remote`

This module offers all the objects, methods, and functions for operations on remote hosts accessible via _SSH/SFTP_ or _FTP_ and a limited support of _CIFS_:
- Execution of commands on a remote host
- Copying directories/files to a remote host
- Deleting directories/files on a remote host
- Copying files between remote hosts (with the local machine acting as a buffer)
- ...

The `scrippy_remote.remote` module provides several objects for transferring files via SFTP, FTP(s), or CIFS, and for remote command execution via SSH.

The source code for the `scrippy_remote.remote` module and its sub-modules is also extensively commented and remains the best source of documentation.

#### SSH/SFTP

##### Execute a command on a remote host:

```python
import logging
from scrippy_remote import remote

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"

with remote.Ssh(username=remote_user,
                hostname=remote_host,
                port=remote_port,
                key_filename=key_filename,
                password=password) as host:
  stdout = host.exec_command("ls /home/luigi.vercotti", return_stdout=True)
  if stdout["exit_code"] == 0:
    for line in stdout["stdout"]:
      logging.debug(line)
```

##### Retrieve a remote file:

```python
import logging
from scrippy_remote.remote import Ssh
from scrippy_remote import ScrippyRemoteError

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
remote_path = "/home/luigi.vercotti/piranha_brothers_files"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"
local_path = "/home/harry.fink"
pattern = ".*"
recursive = True
delete = False
exit_on_error = True

with remote.Ssh(username=remote_user,
                hostname=remote_host,
                port=remote_port,
                key_filename=key_filename,
                password=password) as host:
  try:
    err = host.sftp_get(remote_path=remote_path,
                        local_path=local_path,
                        pattern=pattern,
                        recursive=recursive,
                        delete=delete,
                        exit_on_error=exit_on_error)
    logging.debug("Errors: {}".format(err))
  except ScrippyRemoteError as e:
    logging.critical("{}".format(e))
```

##### Transfer files to a remote host:

```python
from scrippy_remote.remote import Ssh
from scrippy_remote import ScrippyRemoteError

remote_host = "srv.flying.circus"
remote_port = 22
remote_user = "luigi.vercotti"
remote_path = "/home/luigi.vercotti"
key_filename = "/home/luigi.vercotti/.ssh/id_rsa"
password = "dead_parrot"
local_path = "/home/harry.fink"
pattern = ".*"
recursive = True
delete = True
exit_on_error = True

with Ssh(username=remote_user,
         hostname=remote_host,
         port=remote_port,
         key_filename=key_filename) as host:
  try:
    err = host.sftp_put(local_path=local_path,
                        remote_path=remote_path,
                        pattern=pattern,
                        recursive=recursive,
                        delete=delete,
                        exit_on_error=exit_on_error)
    logging.debug("Errors: {}".format(err))
  except ScrippyRemoteError as e:
    logging.critical("{}".format(e))
```

#### FTP

##### Sending a file

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
local_file = "/home/luiggi.vercotti/parrot.txt"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False
# If `ftp_create_dir` is set to `True`, the local tree will be recreated on the remote host
ftp_create_dir = True

# Copy the local file "/home/luiggi.vercotti/parrot.txt" to the remote directory "dead/parrot/home/luiggi.vercotti"
with Ftp(username=remote_user, hostname=remote_host, port=remote_port, password=password, tls=ftp_tls, explicit=ftp_explicit_tls, ssl_verify=ftp_ssl_verify) as host:
  host.put_file(local_file=local_file, remote_dir=remote_dir, create_dir=ftp_create_dir)
```

##### Listing files in a remote directory

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
# Pattern is a regular expression
pattern = ".*\.txt"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

# List all *.txt files in the remote directory "dead/parrot"
with Ftp(username=remote_user, hostname=remote_host, port=remote_port, password=password, tls=ftp_tls, explicit=ftp_explicit_tls, ssl_verify=ftp_ssl_verify) as host:
    files = host.list(remote_dir=remote_dir, pattern=pattern)
```


##### Retrieving a remote file

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
remote_file = "parrot.txt"
local_dir = "/home/luiggi.vercotti"
# If `ftp_create_dir` is set to `True`, the remote tree will be recreated on the local host
ftp_create_dir = True
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user, hostname=remote_host, port=remote_port, password=password, tls=ftp_tls, explicit=ftp_explicit_tls, ssl_verify=ftp_ssl_verify) as host:
  remote_file = os.path.join(remote_dir, remote_file)
  host.get_file(remote_file=remote_file, local_dir=local_dir, create_dir=ftp_create_dir)
```

##### Deleting a remote file

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
remote_file = "parrot.txt"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user, hostname=remote_host, port=remote_port, password=password, tls=ftp_tls, explicit=ftp_explicit_tls, ssl_verify=ftp_ssl_verify) as host:
  remote_file = os.path.join(remote_dir, remote_file)
  host.delete_remote_file(remote_file)
```

##### Deleting a remote directory

The directory will only be deleted if it is empty.

```python
remote_host = "srv.flying.circus"
remote_port = 21
remote_user = "luiggi.vercotti"
remote_dir = "dead/parrot"
password = "d34dp4rr0t"
ftp_tls = True
ftp_explicit_tls = True
ftp_ssl_verify = False

with Ftp(username=remote_user, hostname=remote_host, port=remote_port, password=password, tls=ftp_tls, explicit=ftp_explicit_tls, ssl_verify=ftp_ssl_verify) as host:
  host.delete_remote_dir(remote_dir)
```

---

#### CIFS

Usage example:

```python
with Cifs(
  hostname='SRV2GNC.gnc.recif.nc',
  shared_folder='BackupConfluence',
  username='svc.conf-bkp',
  password='MonSuperMotDePasse') as cifs:

  cifs.create_directory('myfolder')

  cifs.put_file(local_filepath='./mlocal-file.txt', remote_filepath='myfolder/remote-file.txt')

  cifs.get_file(remote_filepath='myfolder/remote-file.txt', local_filepath='./copy.txt')

  with cifs.open_for_write('myfolder/new-remote-file.txt') as file:
    file.write(b'Hello from cifs.open_for_write')

  with cifs.open_for_read('myfolder/new-remote-file.txt') as file:
    print(file.readlines())

  cifs.delete_directory_content('myfolder')
```

---
