"""Scrippy basic POP3 client"""
import time
import socket
from io import BytesIO
from scrippy_mail import ScrippyMailError, logger


class PopClient:
  """
  The PopClient class implements a portion of the POP3 protocol (RFC 1939).

  https://tools.ietf.org/html/rfc1939

  By default, the POP3 server used is the local machine '127.0.0.1'.
  """

  def __init__(self, host='127.0.0.1', port=110, timeout=2):
    self.host = host
    self.port = port
    self.timeout = timeout
    self.socket = None

  def connect(self):
    """Connect to remote server."""
    logger.debug(f"[+] Connecting to POP server: {self.host}:{self.port}")
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(self.timeout)
    try:
      self.socket.connect((self.host, self.port))
      self._recv_data()
    except Exception as err:
      err_msg = f"Error while connecting: [{err.__class__.__name__}] {err}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyMailError(err_msg) from err

  def _send_data(self, data):
    """
    Sends the data passed as argument to the remote server via the socket.
    This method is for internal use and should not be used directly
    """
    try:
      self.socket.sendall(data)
      logger.debug(f"Sent: {data}")
    except Exception as err:
      err_msg = f"Error while communicating with remote server: [{err.__class__.__name__}]: {err}"
      logger.critical(err_msg)
      raise ScrippyMailError(err_msg) from err

  def _recv_data(self, bufsize=8192):
    """
    Receives the data sent by the remote server through the socket.
    This method is for internal use and should not be used directly.
    """
    data = b''
    start = time.time()
    try:
      # Retry until timeout
      while time.time() - start < self.timeout:
        try:
          packet = self.socket.recv(bufsize)
          data += packet
        except Exception as err:
          logger.debug(f"{time.time() - start}/{self.timeout}")
          logger.debug(f"{err.__class__.__name__}]: {err}")
      logger.debug(f"Received: {data}")
      return data
    except Exception as err:
      err_msg = f"Error while communicating with remote server: [{err.__class__.__name__}]: {err}"
      raise ScrippyMailError(err_msg) from err

  def authenticate(self, username, password):
    """
    User authentication.
    Raises a ScrippyMailError error if authentication fails.
    """
    logger.debug(f"[+] Auhentication: {username}:{password}")
    buffer = BytesIO()
    buffer.write(b'USER %s\r\n' % username.encode())
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Authentication error: {resp}"
      logger.critical(f" '-> {err_msg}")
      raise ScrippyMailError(err_msg)
    buffer = BytesIO()
    buffer.write(b'PASS %s\r\n' % password.encode())
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Authentication error: {resp}"
      raise ScrippyMailError(err_msg)

  def stat(self):
    """
    Retrieves the number of messages available in user's mailbox.
    Raises a ScrippyMailError error if authentication fails.
    """
    logger.debug("[+] Getting available mails number")
    buffer = BytesIO()
    buffer.write(b'STAT\r\n')
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Error while communicating with remote server: {resp}"
      raise ScrippyMailError(err_msg)
    return resp

  def retr(self, num):
    """
    Retrieves the content of the email with the number passed as an argument.
    Raises a ScrippyMailError error if authentication fails.
    """
    logger.debug(f"[+] Getting email number: {num}")
    buffer = BytesIO()
    buffer.write(b'RETR %d\r\n' % num)
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Error while communicating with remote server: {resp}"
      raise ScrippyMailError(err_msg)
    # Returns only the email (without server response code)
    return resp.split(b'\r\n', 1)[1]

  def dele(self, num):
    """
    Deletes the content of the email with the number passed as an argument.
    Raises a ScrippyMailError error if authentication fails.
    """
    logger.debug(f"[+] Deleting email number: {num}")
    buffer = BytesIO()
    buffer.write(b'DELE %d\r\n' % num)
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Error while communicating with remote server: {resp}"
      raise ScrippyMailError(err_msg)
    return resp

  def bye(self):
    """Deconnect from remte server."""
    logger.debug("[+] Disconnecting from email server")
    buffer = BytesIO()
    buffer.write(b'QUIT\r\n')
    self._send_data(buffer.getvalue())
    self.socket.shutdown(socket.SHUT_WR)
