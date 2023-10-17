import os
import ssl
import smtplib
import mimetypes
from email.utils import make_msgid, localtime
from email.message import EmailMessage
from email.headerregistry import Address
from scrippy_mail import ScrippyMailError, logger
from scrippy_mail.ciphers import DEFAULT_CIPHERS


class Client:
  """This class purpose is to provide a basic SMTP client able to perform outgoing email operations (i.e. send mail to recipients) using the SMTP protocol.

  Arguments:

    ``username``: String. Optional. The user name used for authentication on remote SMTP server if needed.
    ``password``: String. Optional, The password used for authentication on remote SMTP server if needed.
    ``host``: String. Optional. The remote SMTP server to connect to. Default to ``localhost``
    ``port``: Int. Optional. The TCP remote port to connect to. Default to ``25``.
    ``ssl``: Boolean. Optional. When set to ``True``, the connection will use a SSL encrypted socket. Default to ``False``.
    ``starttls``: Boolean. Optional. When set to ``True``, SSL negotiation will done using the ``STARTTLS`` command. Default to ``False``.
    ``ssl_verify``: Boolean. Optional. Whether the remote server SSL certificate must be verified when using ``ssl`` or ``starttls``. Default to ``True``.
    ``timeout``: Int. Optional. The connection timeout. Default to ``60``.
    ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will be logged as a warning. When set to ``True``, exit the workflow if any error is encountered. Default: ``True``.

    Note: The ``ssl`` and ``starttls`` arguments are mutually exclusive. You may user either one of them or none but not both at the same time.
  """
  @property
  def connected(self):
    return self.client is not None and self._connected

  def __init__(self, host, port=110, username=None, password=None,
               ssl=False, starttls=False, ssl_verify=True,
               timeout=60, exit_on_error=True):
    self.client = None
    self._connected = False
    self.username = username
    self.password = password
    self.host = host
    self.port = port
    self.ssl = ssl
    self.starttls = starttls
    self.ssl_verify = ssl_verify
    self.timeout = timeout
    self.exit_on_error = exit_on_error

  def __enter__(self):
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    self._close()

  def connect(self):
    if not self.connected:
      try:
        self._connect()
      except (ConnectionRefusedError,
              smtplib.SMTPHeloError,
              smtplib.SMTPAuthenticationError,
              smtplib.SMTPNotSupportedError,
              smtplib.SMTPException) as err:
        err_msg = f"{err.__class__.__name__} {err}"
        if isinstance(err, smtplib.SMTPException):
          err_msg = f"[{err.__class__.__name__} {err.smtp_code} {err.smtp_error.decode('utf-8')}"
        if self.exit_on_error:
          logger.critical(err_msg)
          raise err
        logger.warning(err_msg)

  def _connect(self):
    if self.ssl or self.starttls:
      logger.info("Creating secure connection...")
      ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
      ctx.options |= ssl.OP_NO_SSLv2
      ctx.options |= ssl.OP_NO_SSLv3
      ctx.set_ciphers(DEFAULT_CIPHERS)
      ctx.check_hostname = False
      ctx.verify_mode = ssl.CERT_NONE
      if self.ssl_verify:
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = True
        ctx.set_default_verify_paths()
        ctx.load_default_certs()
    logger.info(f"Connecting to {self.host}:{self.port}")
    if self.ssl:
      self.client = smtplib.SMTP_SSL(self.host,
                                     self.port,
                                     self.timeout,
                                     context=ctx)
    else:
      self.client = smtplib.SMTP(self.host,
                                 self.port,
                                 self.timeout)
      if self.starttls:
        logger.info("Using STARTTLS")
        response = self.client.starttls(context=ctx)
    if self.starttls is None or self.starttls is False:
      response = self.client.connect(self.host,
                                     self.port)
    self.client.ehlo_or_helo_if_needed()
    if self.username is not None:
      logger.debug("Authentication...")
      try:
        self.client.login(self.username,
                          self.password)
      except Exception as err:
        raise err
    self._connected = True

  def _close(self):
    if self.connected:
      self.client.quit()
    self._connected = False

  def send(self, subject, body, sender, recipients=None,
           cc=None, bcc=None, attachments=None):
    """Send the email to specified recipients.

    Arguments:
      ``subject``: String. The email subject.
      ``body``: String. The email body.
      ``sender``: String. The email sender email address.
      ``Recipients``: List. Optional. List of email email addresses for recipients (To).
      ``cc``: List. Optional. List of email addresses for `carbon copy` recipients.
      ``bcc``: List. Optional. List of email addresses for `blind carbon copy` recipients.
      ``attachments``: List. Optional. List of file names to be attached to the email.
    """
    logger.info("Sending email...")
    envelope = self._pack(subject, body, sender, recipients,
                          cc, bcc, attachments)
    try:
      if not self.connected:
        self.connect()
      result = self.client.send_message(envelope)
      if len(result) > 0:
        rejects = "\n".join([f"Rejected: <{reject[0]}> Reason: [{reject[1][0]}] {reject[1][1].decode('utf-8')}" for reject in result.items()])
        raise ScrippyMailError(rejects)
    except Exception as err:
      err_msg = f"[SmtpSendError] {err.__class__.__name__} {err}"
      if isinstance(err, smtplib.SMTPRecipientsRefused):
        # Ignore pylint error about inexistent err.recipients attribute
        refused = "\n".join([f"{rcpt}: {reason[0]} {reason[1].decode('utf-8')}"
                             for rcpt, reason in err.recipients.items()])
        err_msg = f"[SmtpSendError] {err.__class__.__name__} {refused}"
      if self.exit_on_error:
        logger.critical(err_msg)
        raise ScrippyMailError(err_msg) from err
      logger.warning(err_msg)

  def _pack(self, subject, body, sender, recipients=None,
            cc=None, bcc=None, attachments=None):
    """Create message envelope from given arguments.

    Raises:
      ``ScrippyMailError`` When ``recipients``, ``cc``, ``bcc`` are all set to ``None``.
    """
    if all([recipients is None, cc is None, bcc is None]):
      raise ScrippyMailError("[SmtpEnvelopeError] One of recipients, cc or bcc must be filled")
    attachments = attachments or list()
    envelope = EmailMessage()
    envelope["Subject"] = subject
    envelope["Sender"] = Address(addr_spec=sender)
    envelope["From"] = Address(addr_spec=sender)
    if recipients is not None:
      envelope["To"] = [Address(addr_spec=recipient)
                        for recipient in recipients]
    if cc is not None:
      envelope["Cc"] = [Address(addr_spec=c) for c in cc]
    if bcc is not None:
      envelope["Bcc"] = [Address(addr_spec=c) for c in bcc]
    envelope["Date"] = localtime()
    envelope["Message-ID"] = make_msgid()
    envelope["User-Agent"] = "Scrippy MUA"
    envelope.set_content(body)
    for attachment in attachments:
      maintype, subtype = self._get_mime_type(attachment)
      envelope.add_attachment(open(attachment, mode="rb").read(),
                              maintype=maintype,
                              subtype=subtype,
                              filename=os.path.basename(attachment))
    return envelope

  def _get_mime_type(self, filename):
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
      ctype = 'application/octet-stream'
    return ctype.split('/', 1)
