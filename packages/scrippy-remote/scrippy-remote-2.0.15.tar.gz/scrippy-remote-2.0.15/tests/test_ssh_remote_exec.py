"""Module de test scrippy_remote.remote.Ssh."""
import os
import re
from scrippy_remote.remote import Ssh

remote_host = "sshd"
remote_port = 2200
remote_user = "scrippy"
remote_path = "/home/scrippy"
key_filename = f"{os.path.dirname(os.path.realpath(__file__))}/ssh/scrippy.rsa"
local_path = "/tmp"
test_filename = "inquisition.txt"
pattern = f".*{test_filename}"


def test_remote_exec():
  with Ssh(username=remote_user,
           hostname=remote_host,
           port=remote_port,
           key_filename=key_filename) as host:
    stdout = host.exec_command(f"ls {remote_path}", return_stdout=True)
    assert stdout["exit_code"] == 0
    for line in stdout["stdout"]:
      if re.match(pattern, line):
        return True
    return False
