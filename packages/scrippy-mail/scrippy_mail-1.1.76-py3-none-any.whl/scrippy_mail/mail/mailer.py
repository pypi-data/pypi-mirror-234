"""Scrippy SMTP client."""
import ssl
import smtplib
from datetime import datetime
from email.utils import make_msgid
from email.message import EmailMessage
from scrippy_mail import logger


_DEFAULT_CIPHERS = ('ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:'
                    'ECDH+AES128:DH+AES:ECDH+HIGH:'
                    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:'
                    'RSA+HIGH:RSA+3DES:!aNULL:'
                    '!eNULL:!MD5'
                    )


class Mailer:
  """
  The Mailer object is a simplified interface to the smtplib library for sending emails that comply with the current RFC standards.

  By default, the Mailer class uses the local machine and port 25 as the SMTP server.
  """

  def __init__(self, host='localhost', port=25,
               user=None, password=None,
               ssl=False, starttls=False, timeout=60):
    self.host = host
    self.port = port
    self.user = user
    self.password = password
    self.ssl = ssl
    self.starttls = starttls
    self.timeout = timeout
    self.smtp = None
    assert not (self.ssl and self.starttls)

  def send(self, subject, body, to_addrs, from_addr):
    """Sends the email with the parameters passed as arguments."""
    logger.debug(f"[+] Sending email to {', '.join(to_addrs)}")
    if not isinstance(to_addrs, tuple):
      to_addrs = (to_addrs,)
    tzone = f"{datetime.now().astimezone().tzinfo}00"
    date = datetime.today().strftime("%a, %d %b %Y %H:%M:%S {}").format(tzone)
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = from_addr
    message['To'] = to_addrs
    message['Date'] = date
    message['Message-ID'] = make_msgid()
    message.set_content(body)
    logger.debug("[+] Sending email:")
    logger.debug(f" '-> Host: {self.host}:{self.port}")
    logger.debug(f" '-> User: {self.user} [{self.password}]")
    logger.debug(f" '-> To: {to_addrs}")
    logger.debug(f" '-> From: {from_addr}")
    logger.debug(f" '-> Subject: {subject}")
    try:
      if self.ssl or self.starttls:
        logger.debug(" '-> SSL Context creation")
        # FIXME: Trouver le moyen de vérifier le certificat serveur à partir des CA installées sur le système:
        # https://docs.python.org/3/library/ssl.html#best-defaults
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.set_ciphers(_DEFAULT_CIPHERS)
        context.set_default_verify_paths()
        context.load_default_certs()
        # context.verify_mode = ssl.CERT_REQUIRED
        context.verify_mode = ssl.CERT_NONE
      if self.ssl:
        self.smtp = smtplib.SMTP_SSL(self.host, self.port, self.timeout, context=context)
      else:
        self.smtp = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
      with self.smtp:
        if self.starttls:
          logger.debug(" '-> STARTTLS...")
          response = self.smtp.starttls(context=context)
          logger.debug(f"  '-> {response}")
        else:
          logger.debug(" '-> Connecting...")
          response = self.smtp.connect(self.host, self.port)
          logger.debug(f"  '-> {response[0]}: {response[1]}")
        self.smtp.ehlo_or_helo_if_needed()
        if self.user:
          logger.debug(" '-> Authentication...")
          self.smtp.login(self.user, self.password)
        logger.debug(" '-> Sending mail...")
        result = self.smtp.send_message(message, from_addr, to_addrs)
        if result:
          for reject in result:
            logger.error(f" '-> {reject}: {result[reject][0]}: {result[reject][1]}")
        logger.debug(" '-> Bye...")
        self.smtp.quit()
        if result:
          return False
        return True
    except (ConnectionRefusedError, smtplib.SMTPHeloError,
            smtplib.SMTPAuthenticationError, smtplib.SMTPNotSupportedError,
            smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused, smtplib.SMTPDataError, smtplib.SMTPException, RuntimeError) as err:
      logger.error(f"[{err.__class__.__name__}] {err}")
      return False
    except Exception as err:
      logger.error(f"[{err.__class__.__name__}] {err}")
      return False
