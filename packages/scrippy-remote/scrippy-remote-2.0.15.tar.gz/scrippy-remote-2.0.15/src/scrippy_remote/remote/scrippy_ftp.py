"""
Réecriture de la classe FTP fournie par ftplib afin de permettre le FTPes
ainsi que le FTPS sur n'importe quel port TCP.

© 2020 - MCO System - https://www.mcos.nc
"""
import re
import ssl
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT
from scrippy_remote import logger

# ------------------------------------------------------------------------------
# Some constants: 'Don't touch that, you little rascal©'
# ------------------------------------------------------------------------------
CRLF = '\r\n'
B_CRLF = b'\r\n'
MSG_OOB = 0x1


# ------------------------------------------------------------------------------
# Specific error classes
# ------------------------------------------------------------------------------
class Error(Exception):
  pass


class ErrorReply(Error):
  pass


class ErrorTemp(Error):
  pass


class ErrorPerm(Error):
  pass


class ErrorProto(Error):
  pass


# ------------------------------------------------------------------------------
# Some functions for parsing received responses.
# ------------------------------------------------------------------------------
def sanitize(message):
  if message[:5] in {'pass ', 'PASS '}:
    i = len(message.rstrip('\r\n'))
    message = message[:5] + '*' * (i - 5) + message[i:]
  return repr(message)


def parse150(resp):
  if resp[:3] != '150':
    raise ErrorReply(resp)
  reg_150 = re.compile(r"150 .* \((\d+) bytes\)", re.IGNORECASE | re.ASCII)
  m = reg_150.match(resp)
  if not m:
    return None
  return int(m.group(1))


def parse227(resp):
  if resp[:3] != '227':
    raise ErrorReply(resp)
  reg_227 = re.compile(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', re.ASCII)
  m = reg_227.search(resp)
  if not m:
    raise ErrorProto(resp)
  numbers = m.groups()
  host = '.'.join(numbers[:4])
  port = (int(numbers[4]) << 8) + int(numbers[5])
  return host, port


def parse229(resp, peer):
  if resp[:3] != '229':
    raise ErrorReply(resp)
  left = resp.find('(')
  if left < 0:
    raise ErrorProto(resp)
  right = resp.find(')', left + 1)
  if right < 0:
    raise ErrorProto(resp)
  if resp[left + 1] != resp[right - 1]:
    raise ErrorProto(resp)
  parts = resp[left + 1:right].split(resp[left + 1])
  if len(parts) != 5:
    raise ErrorProto(resp)
  host = peer[0]
  port = int(parts[3])
  return host, port


def parse257(resp):
  if resp[:3] != '257':
    raise ErrorReply(resp)
  if resp[3:5] != ' "':
    return ''
  dirname = ''
  i = 5
  n = len(resp)
  while i < n:
    c = resp[i]
    i = i + 1
    if c == '"':
      if i >= n or resp[i] != '"':
        break
      i = i + 1
    dirname = dirname + c
  return dirname


def print_line(line):
  print(line)


class FtpSimple:
  """
  The basic FTP class without any SSL support.
  This class implements all the basic features of the FTP protocol.
  This class serves as the parent class for the Ftps and Ftpes classes.
  """

  ENCODING = 'latin-1'
  maxline = 8192
  sock = None
  af = None
  file = None
  welcome = None
  passive = 1

  def __init__(self, hostname, port=21,
               username='anonymous', password='anonymous',
               timeout=_GLOBAL_DEFAULT_TIMEOUT):
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    self.timeout = timeout

  def __enter__(self):
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    del type_err, value, traceback
    self.close()

  def connect(self):
    logger.debug("[+] Connection")
    if self.hostname is not None:
      self.sock = socket.create_connection((self.hostname, self.port),
                                           self.timeout)
      self.af = self.sock.family
      self.file = self.sock.makefile('r', encoding=self.ENCODING)
      logger.debug(f"[WELCOME] {self._getresp()}")
      logger.debug("[=] connected")
      return True
    raise Error("Remote host not defined")

  def login(self):
    resp = self.sendcmd(f"USER {self.username}")
    if resp[0] == '3':
      resp = self.sendcmd(f"PASS {self.password}")
    if resp[0] != '2':
      raise ErrorReply(resp)
    logger.debug("[=] Logged in")
    return resp

  def _putline(self, line):
    if '\r' in line or '\n' in line:
      raise ValueError("Illegal newline character should not be contained")
    line = line + CRLF
    self.sock.sendall(line.encode(self.ENCODING))

  def _getline(self):
    line = self.file.readline(self.maxline + 1)
    if len(line) > self.maxline:
      raise Error(f"got more than {self.maxline} bytes")
    if not line:
      raise EOFError
    if line[-2:] == CRLF:
      line = line[:-2]
    elif line[-1:] in CRLF:
      line = line[:-1]
    return line

  def _putcmd(self, line):
    logger.debug(f"[CMD] {sanitize(line)}")
    self._putline(line)

  def _getmultiline(self):
    line = self._getline()
    if line[3:4] == '-':
      code = line[:3]
      while 1:
        nextline = self._getline()
        line += (f"\n{nextline}")
        if nextline[:3] == code and nextline[3:4] != '-':
          break
    return line

  def _getresp(self):
    resp = self._getmultiline()
    logger.debug(f"[RESP] {sanitize(resp)}")
    c = resp[:1]
    if c in {'1', '2', '3'}:
      return resp
    if c == '4':
      raise ErrorTemp(resp)
    if c == '5':
      raise ErrorPerm(resp)
    raise ErrorProto(resp)

  def _voidresp(self):
    resp = self._getresp()
    if resp[:1] != '2':
      raise ErrorReply(resp)
    return resp

  def sendcmd(self, cmd):
    self._putcmd(cmd)
    return self._getresp()

  def voidcmd(self, cmd):
    self._putcmd(cmd)
    return self._voidresp()

  def set_pasv(self, value):
    self.passive = value

  def sendport(self, host, port):
    hbytes = host.split('.')
    pbytes = [repr(port // 256), repr(port % 256)]
    tbytes = hbytes + pbytes
    cmd = f"PORT {','.join(tbytes)}"
    return self.voidcmd(cmd)

  def sendeprt(self, host, port):
    '''Send an EPRT command with the current host and the given port number.'''
    af = 0
    if self.af == socket.AF_INET:
      af = 1
    if self.af == socket.AF_INET6:
      af = 2
    if af == 0:
      raise ErrorProto('unsupported address family')
    fields = ['', repr(af), host, repr(port), '']
    cmd = f"EPRT {'|'.join(fields)}"
    return self.voidcmd(cmd)

  def makeport(self):
    err = None
    sock = None
    for res in socket.getaddrinfo(None, 0,
                                  self.af,
                                  socket.SOCK_STREAM, 0,
                                  socket.AI_PASSIVE):
      af, socktype, proto, canonname, sa = res
      try:
        sock = socket.socket(af, socktype, proto)
        sock.bind(sa)
      except OSError as _:
        err = _
        if sock:
          sock.close()
        sock = None
        continue
      break
    if sock is None:
      if err is not None:
        raise err
      raise OSError("getaddrinfo returns an empty list")
    sock.listen(1)
    port = sock.getsockname()[1]
    host = self.sock.getsockname()[0]
    if self.af == socket.AF_INET:
      resp = self.sendport(host, port)
    else:
      resp = self.sendeprt(host, port)
      sock.settimeout(self.timeout)
    return sock

  def makepasv(self):
    if self.af == socket.AF_INET:
      host, port = parse227(self.sendcmd('PASV'))
    else:
      host, port = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
    return host, port

  def ntransfercmd(self, cmd, rest=None):
    size = None
    if self.passive:
      host, port = self.makepasv()
      logger.debug(f"[PASV] {host}:{port}")
      conn = socket.create_connection((host, port), self.timeout)
      try:
        if rest is not None:
          self.sendcmd(f"REST {rest}")
        resp = self.sendcmd(cmd)
        if resp[0] == '2':
          resp = self._getresp()
        if resp[0] != '1':
          raise ErrorReply(resp)
      except Exception:
        conn.close()
        raise
    else:
      with self.makeport() as sock:
        if rest is not None:
          self.sendcmd(f"REST {rest}")
        resp = self.sendcmd(cmd)
        if resp[0] == '2':
          resp = self._getresp()
        if resp[0] != '1':
          raise ErrorReply(resp)
        conn, sockaddr = sock.accept()
        if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
          conn.settimeout(self.timeout)
    if resp[:3] == '150':
      size = parse150(resp)
    return conn, size

  def transfercmd(self, cmd, rest=None):
    return self.ntransfercmd(cmd, rest)[0]

  def retrbinary(self, cmd, callback, blocksize=8192, rest=None):
    self.voidcmd('TYPE I')
    with self.transfercmd(cmd, rest) as conn:
      while 1:
        data = conn.recv(blocksize)
        if not data:
          break
        callback(data)
    return self._voidresp()

  def retrlines(self, cmd, callback=None):
    if callback is None:
      callback = print_line
    resp = self.sendcmd('TYPE A')
    with self.transfercmd(cmd) as conn, \
         conn.makefile('r', encoding=self.ENCODING) as fp:
      while 1:
        line = fp.readline(self.maxline + 1)
        if len(line) > self.maxline:
          raise Error(f"got more than {self.maxline} bytes")
        logger.debug(f"[RETR] {repr(line)}")
        if not line:
          break
        if line[-2:] == CRLF:
          line = line[:-2]
        elif line[-1:] == '\n':
          line = line[:-1]
        callback(line)
    return self._voidresp()

  def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
    self.voidcmd('TYPE I')
    with self.transfercmd(cmd, rest) as conn:
      while 1:
        buf = fp.read(blocksize)
        if not buf:
          logger.debug("[STOR] EOF")
          break
        conn.sendall(buf)
        if callback:
          callback(buf)
    return self._voidresp()

  def storlines(self, cmd, fp, callback=None):
    self.voidcmd('TYPE A')
    with self.transfercmd(cmd) as conn:
      while 1:
        buf = fp.readline(self.maxline + 1)
        if len(buf) > self.maxline:
          raise Error(f"got more than {self.maxline} bytes")
        if not buf:
          break
        if buf[-2:] != B_CRLF:
          if buf[-1] in B_CRLF:
            buf = buf[:-1]
            buf = buf + B_CRLF
        conn.sendall(buf)
        if callback:
          callback(buf)
    return self._voidresp()

  def nlst(self, *args):
    cmd = 'NLST'
    for arg in args:
      cmd = f"{cmd} {arg}"
    files = []
    self.retrlines(cmd, files.append)
    return files

  def dir(self, *args):
    cmd = 'LIST'
    func = None
    if args[-1:] and isinstance(args[-1], str):
      args, func = args[:-1], args[-1]
    for arg in args:
      if arg:
        cmd = f"{cmd} {arg}"
    self.retrlines(cmd, func)

  def mlsd(self, path="", facts=None):
    if facts is None:
      facts = []
    if facts:
      self.sendcmd("OPTS MLST " + ";".join(facts) + ";")
    if path:
      cmd = f"MLSD {path}"
    else:
      cmd = "MLSD"
    lines = []
    self.retrlines(cmd, lines.append)
    for line in lines:
      facts_found, _, name = line.rstrip(CRLF).partition(' ')
      entry = {}
      for fact in facts_found[:-1].split(";"):
        key, _, value = fact.partition("=")
        entry[key.lower()] = value
      yield (name, entry)

  def rename(self, fromname, toname):
    resp = self.sendcmd(f"RNFR {fromname}")
    if resp[0] != '3':
      raise ErrorReply(resp)
    return self.voidcmd(f"RNTO {toname}")

  def delete(self, filename):
    resp = self.sendcmd(f"DELE {filename}")
    if resp[:3] in {'250', '200'}:
      return resp
    raise ErrorReply(resp)

  def cwd(self, dirname):
    if dirname == '..':
      try:
        return self.voidcmd('CDUP')
      except ErrorPerm as msg:
        if msg.args[0][:3] != '500':
          raise
    elif dirname == '':
      dirname = '.'
    cmd = f"CWD {dirname}"
    return self.voidcmd(cmd)

  def size(self, filename):
    resp = self.sendcmd(f"SIZE {filename}")
    if resp[:3] == '213':
      s = resp[3:].strip()
      return int(s)
    raise ErrorReply(resp)

  def mkd(self, dirname):
    resp = self.voidcmd(f"MKD {dirname}")
    if not resp.startswith('257'):
      return ''
    return parse257(resp)

  def rmd(self, dirname):
    return self.voidcmd(f"RMD {dirname}")

  def pwd(self):
    resp = self.voidcmd('PWD')
    if not resp.startswith('257'):
      return ''
    return parse257(resp)

  def quit(self):
    resp = self.voidcmd('QUIT')
    self.close()
    return resp

  def close(self):
    logger.debug("[CLOSE]")
    self.file.close()
    self.sock.close()


class Ftps(FtpSimple):
  """
  This class extends the Ftp class by adding support for FTP over implicit TLS.
  """

  ssl_version = None
  ssl_verify = True
  context = None
  _prot_p = False

  def __init__(self, hostname, port=21,
               username='anonymous', password='anonymous',
               ssl_verify=True, ssl_version=ssl.PROTOCOL_TLSv1_2):
    super().__init__(hostname=hostname, port=port,
                     username=username, password=password)
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl_version
    self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    if not self.ssl_verify:
      self.context.check_hostname = False
      self.context.verify_mode = ssl.CERT_NONE

  def connect(self):
    logger.debug("[+] Connection (Implicit TLS)")
    if self.hostname is not None:
      self.sock = socket.create_connection((self.hostname, self.port),
                                           self.timeout)
      self.af = self.sock.family
      if not self.ssl_verify:
        logger.warning("[!] Insecure connection: ssl_verify set to False")
      self.sock = self.context.wrap_socket(self.sock,
                                           server_hostname=self.hostname)
      self.file = self.sock.makefile('r', encoding=self.ENCODING)
      logger.debug(f"[WELCOME] {self._getresp()}")
      logger.debug("[=] connected")
      return True
    raise Error("Remote host not defined")

  def ntransfercmd(self, cmd, rest=None):
    conn, size = super().ntransfercmd(cmd, rest)
    if self._prot_p:
      conn = self.context.wrap_socket(conn,
                                      server_hostname=self.hostname,
                                      session=self.sock.session)
    return conn, size

  def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
    self.prot_p()
    self.voidcmd('TYPE I')
    conn = self.transfercmd(cmd, rest)
    while 1:
      buf = fp.read(blocksize)
      if not buf:
        logger.debug("[STOR] EOF")
        break
      conn.sendall(buf)
      if callback:
        callback(buf)
    conn.unwrap()
    return self._voidresp()

  def storlines(self, cmd, fp, callback=None):
    self.prot_p()
    self.voidcmd('TYPE A')
    conn = self.transfercmd(cmd)
    while 1:
      buf = fp.readline(self.maxline + 1)
      if len(buf) > self.maxline:
        raise Error(f"got more than {self.maxline} bytes")
      if not buf:
        break
      if buf[-2:] != B_CRLF:
        if buf[-1] in B_CRLF:
          buf = buf[:-1]
          buf = buf + B_CRLF
      conn.sendall(buf)
      if callback:
        callback(buf)
    conn.unwrap()
    return self._voidresp()

  def retrbinary(self, cmd, callback, blocksize=8192, rest=None):
    self.prot_p()
    self.voidcmd('TYPE I')
    conn = self.transfercmd(cmd, rest)
    while 1:
      data = conn.recv(blocksize)
      if not data:
        break
      callback(data)
    conn.unwrap()
    return self._voidresp()

  def retrlines(self, cmd, callback=None):
    self.prot_p()
    if callback is None:
      callback = print_line
    resp = self.sendcmd('TYPE A')
    conn = self.transfercmd(cmd)
    with conn.makefile('r', encoding=self.ENCODING) as fp:
      while 1:
        line = fp.readline(self.maxline + 1)
        if len(line) > self.maxline:
          raise Error(f"got more than {self.maxline} bytes")
        logger.debug(f"[RETR] {repr(line)}")
        if not line:
          break
        if line[-2:] == CRLF:
          line = line[:-2]
        elif line[-1:] == '\n':
          line = line[:-1]
        callback(line)
    conn.unwrap()
    return self._voidresp()

  def close(self):
    logger.debug("[CLOSE]")
    self.file.close()
    try:
      self.sock.unwrap()
    except Exception:
      pass
    self.sock.close()

  def ccc(self):
    resp = self.voidcmd('CCC')
    self.sock = self.sock.unwrap()
    return resp

  def prot_p(self):
    self.voidcmd('PBSZ 0')
    resp = self.voidcmd('PROT P')
    self._prot_p = True
    return resp

  def prot_c(self):
    resp = self.voidcmd('PROT C')
    self._prot_p = False
    return resp


class Ftpes(Ftps):
  """
  This class extends the Ftp class by adding support for FTP over explicit TLS.
  """

  ssl_version = None
  ssl_verify = True
  ssl_session = None
  context = None
  _prot_p = False

  def __init__(self, hostname, port=21,
               username='anonymous', password='anonymous',
               ssl_verify=True, ssl_version=ssl.PROTOCOL_TLSv1_2):
    super().__init__(hostname=hostname, port=port,
                     username=username, password=password)
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl_version
    self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    if not self.ssl_verify:
      self.context.check_hostname = False
      self.context.verify_mode = ssl.CERT_NONE

  def connect(self):
    logger.debug("[+] Connection (Explicit TLS)")
    if self.hostname is not None:
      self.sock = socket.create_connection((self.hostname, self.port),
                                           self.timeout)
      self.af = self.sock.family
      if not self.ssl_verify:
        logger.warning("[!] Insecure connection: ssl_verify set to False")
      self.file = self.sock.makefile('r', encoding=self.ENCODING)
      logger.debug(f"[WELCOME] {self._getresp()}")
      self.auth()
      logger.debug("[=] connected")
      return True
    raise Error("Remote host not defined")

  def auth(self):
    if isinstance(self.sock, ssl.SSLSocket):
      raise ValueError("Connection is already secured")
    if self.ssl_version >= ssl.PROTOCOL_TLS:
      resp = self.voidcmd('AUTH TLS')
    else:
      resp = self.voidcmd('AUTH SSL')
    self.sock = self.context.wrap_socket(self.sock,
                                         server_hostname=self.hostname)
    self.file = self.sock.makefile(mode='r', encoding=self.ENCODING)
    return resp
