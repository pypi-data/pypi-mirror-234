"""Scrippy basic SpamAssassin client"""
import time
import socket
from io import BytesIO
from scrippy_mail import ScrippyMailError, logger


class SpamAssassinClient:
  """
  Implementation of a portion of the SpamAssassin protocol.

  https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL

  By default, the SpamAssassin server used is the local machine '127.0.0.1'.
  """

  def __init__(self, host='127.0.0.1', port=783, timeout=2):
    self.host = host
    self.port = port
    self.timeout = timeout
    self.socket = None

  def __enter__(self):
    """Entry point."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Exit point."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """Connect to remote server."""
    logger.debug(f"[+] Connecting to SpamAssassin server: {self.host}:{self.port}")
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(self.timeout)
    self.socket.connect((self.host, self.port))

  def close(self):
    """Ferme la connexion au serveur SpamAssassin."""
    logger.debug("[+] Closing connection to SpamAssassin")
    self.socket.shutdown(socket.SHUT_WR)
    self.socket.close()

  def _send_data(self, data):
    """
    Sends a message (in the SpamAssassin exchange protocol sense) to the SpamAssassin server.

    This method is used by all methods that need to communicate with the SpamAssassin server.

    https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL
    """
    try:
      self.socket.sendall(data)
      logger.debug(f"Sent: {data}")
    except Exception as err:
      err_msg = f"Error while communicating with SpamAssassin server: [{err.__class__.__name__}]: {err}"
      logger.error(err_msg)
      raise ScrippyMailError(err_msg) from err

  def _recv_data(self, bufsize=8192):
    """
    Receive data from SpamAssassin remote server.
    """
    data = b''
    start = time.time()
    while time.time() - start < self.timeout:
      try:
        packet = self.socket.recv(bufsize)
        data += packet
      except Exception as err:
        logger.debug(f"{time.time() - start}/{self.timeout}")
        logger.debug(f"[{err.__class__.__name__}]: {err}")
    logger.debug(f"Received: {data}")
    return data

  def learn(self, mail, mail_type):
    """
    Give the given email to learn to the SpamAssassin remote server.
    mail_type defines if the given email is SPAM or HAM.

    https://svn.apache.org/repos/asf/spamassassin/trunk/spamd/PROTOCOL
    """
    logger.debug(f"[+] Saving email as [{mail_type.upper()}]")
    try:
      buffer = BytesIO()
      buffer.write(b'TELL SPAMC/1.3\r\n')
      buffer.write(b'Content-Length: %d\r\n' % len(mail))
      buffer.write(b'Message-class: %s\r\n' % mail_type.encode())
      buffer.write(b'Set: local, remote\r\n\r\n')
      buffer.write(mail.encode())
      logger.debug(str(buffer.getvalue()))
      self._send_data(buffer.getvalue())
      # Data must be retrieved even if not used
      resp = self._recv_data()
    except Exception as err:
      err_msg = f"Error while learning: [{err.__class__.__name__}]: {err}"
      logger.error(err_msg)
      raise ScrippyMailError(err_msg) from err

  def check_spam(self, mail):
    """
    Check given email for SPAM.

    Returns True if the given email is evaluated as SPAM.
    Returns False if the given email is evaluated as HAM.

    Result and score are notified in the debug log.
    """
    logger.debug("[+] Checking for spam")
    results = {"True": True, "False": False}
    try:
      buffer = BytesIO()
      buffer.write(b'TELL SPAMC/1.3\r\n')
      buffer.write(b'Content-Length: %d\r\n\r\n' % len(mail))
      buffer.write(mail.encode())
      logger.debug(str(buffer.getvalue()))
      self._send_data(buffer.getvalue())
      data = self._recv_data().split("\r\n")
      if data[0].split()[3] == b'OK':
        result = data[1].split()
        score = f"{result[3].decode().strip()}/{result[5].decode().strip()}"
        result = results[result[1].decode().strip()]
        logger.debug(f"Result: {result} | Score: {score}")
        return result
      # If we reach this point, an error has occurred.
      # We throw the exception so that it can be caught further down the line.
      # Don't mess with that, you little rascal©
      # Touche pas à ça p'tit con©
      raise Exception(f"{data}")
    except Exception as err:
      err_msg = f"Error while checking for spam level: [{err.__class__.__name__}]: {err}"
      logger.error(err_msg)
      raise ScrippyMailError(err_msg) from err
