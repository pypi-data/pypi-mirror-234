import ssl
import imaplib
from scrippy_mail.files import save_email
from scrippy_mail.ciphers import DEFAULT_CIPHERS
from scrippy_mail import ScrippyMailError, logger


SEEN_FLAG = "\\Seen"
DELETE_FLAG = "\\Deleted"


class Client:
  """This class' purpose is to provide a basic IMAP client able to manage incoming email operations using the IMAP protocol.

  Arguments:

    ``username``: String. Optional. The user name used for authentication on remote POP3 server if needed.
    ``password``: String. Optional, The password used for authentication on remote POP3 server if needed.
    ``host``: String. Optional. The remote POP3 server to connect to. Default to ``localhost``
    ``port``: Int. Optional. The TCP remote port to connect to. Default to ``143``.
    ``ssl``: Boolean. Optional. When set to ``True``, the connection will use a SSL encrypted socket. Default to ``False``.
    starttls: Boolean. Optional. When set to ``True``, SSL negotiation will done using the ``STARTTLS`` command. Default to ``False``.
    ``ssl_verify``: Boolean. Optional. Whether the remote server SSL certificate must be verified when using ``ssl`` or ``starttls``. Default to ``True``.
    ``timeout``: Int. Optional. The connection timeout. Default to ``60``.
    ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will be logged as a warning. When set to ``True``, exit the if any error is encountered. Default: ``True``.

    Note: The ``ssl`` and ``starttls`` arguments are mutually exclusive. You may user either one of them or none but not both at the same time.
  """
  @property
  def connected(self):
    return self.client is not None and self._connected

  def __init__(self, username, password, host, port=143,
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
    return self

  def connect(self):
    try:
      self._connect()
    except imaplib.IMAP4.error as err:
      err_msg = f"{err.__class__.__name__} {err}"
      if self.exit_on_error:
        logger.critical(err_msg)
        raise err
      logger.warning(err_msg)

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    if self.ssl or self.starttls:
      logger.debug("Creating secure connection...")
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
    logger.debug(f"Connecting to {self.host}:{self.port}")
    if self.ssl:
      self.client = imaplib.IMAP4_SSL(host=self.host,
                                      port=self.port,
                                      timeout=self.timeout,
                                      ssl_context=ctx)
    else:
      self.client = imaplib.IMAP4(host=self.host,
                                  port=self.port,
                                  timeout=self.timeout)
      if self.starttls:
        logger.debug("Using STARTTLS")
        response = self.client.starttls(ssl_context=ctx)
    if self.username is not None:
      logger.debug("Authentication...")
      try:
        self.client.login(user=self.username,
                          password=self.password)
        self.client.enable("UTF8=ACCEPT")
      except Exception as err:
        raise err
    self.client.select()
    self._connected = True

  def _close(self):
    if self.connected:
      try:
        self.client.close()
      except imaplib.IMAP4.error:
        pass
      self.client.logout()
    self._connected = False

  def list_mailbox(self, mailbox="INBOX"):
    """
    List all sub-mailboxes of the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox to browse. Default to ``INBOX``

    Returns:
      ``list``: List of strings. The list of sub-mailboxes (directories) found in the specified mailbox.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    if not self.connected:
      self.connect()
    self.client.select(mailbox=mailbox)
    try:
      logger.debug("Listing available mailboxes...")
      resp, dirs = self.client.lsub(directory=mailbox,
                                    pattern="*")
      return [d.decode('utf-8').split()[2] for d in dirs]
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapListsubError] {err.__class__.__name__}: {err}"
      raise ScrippyMailError(err_msg) from err

  def get_message_count(self, mailbox="INBOX"):
    """Return the number of available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``

    Returns:
      ``int``: Number of available emails on the remote server in the specified mailbox.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      logger.debug("Getting available emails count...")
      self.client.select(mailbox=mailbox)
      resp, data = self.client.search(None, 'ALL')
      return len(data[0].decode("utf-8").split())
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapCountError] {err.__class__.__name__}: {err}"
      raise ScrippyMailError(err_msg) from err

  def get_messages_numbers(self, mailbox="INBOX", tags=None, inverse=False):
    """Return the list of emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

      ..  code-block:: python

        client.get_messages_numbers(mailbox="INBOX",
                                    tags=["Scrippy", "scrangourou"],
                                    inverse=False):

      Will return the list of email numbers tagged ``Scrippy`` or ``scrangourou`` available in the ``INBOX`` mailbox directory.

      ..  code-block:: python

        client.get_messages_numbers(mailbox="INBOX",
                                    tags=["Scrippy", "scrangourou"],
                                    inverse=True):

      Will return the list of email numbers neither tagged ``Scrippy`` or ``scrangourou`` available in the ``INBOX`` mailbox directory.

      If ``tags`` is not specified, the method will return the list of all available emails numbers in the specified mailbox.

    Returns:
      ``list``: List of available emails numbers matching specified criteria and mailbox.

    Raises:
      ``ScrippyMailError``: Notably when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      logger.debug("Getting available mails numbers...")
      self.client.select(mailbox=mailbox)
      resp, data = self.client.search(None, 'ALL')
      uids = [uid for uid in data[0].split()]
      if tags is not None:
        select = list()
        for uid in uids:
          resp, flags = self.client.fetch(uid, "(FLAGS)")
          flags = [flag.decode("utf-8")
                   for flag in imaplib.ParseFlags(flags[0])]
          if inverse:
            if set(tags).isdisjoint(flags):
              select.append(uid)
          else:
            if not set(tags).isdisjoint(flags):
              select.append(uid)
        return select
      return uids
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapListError] {err.__class__.__name__}: {err}"
      raise ScrippyMailError(err_msg) from err

  def get_unread_messages_numbers(self, mailbox="INBOX"):
    """Return the list of unread emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``list``: List of unread emails numbers matching specified mailbox.
    """
    return self.get_messages_numbers(mailbox=mailbox,
                                     tags=[SEEN_FLAG],
                                     inverse=True)

  def get_read_messages_numbers(self, mailbox="INBOX"):
    """Return the list of read emails numbers available emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``list``: List of read emails numbers matching specified mailbox.
    """
    return self.get_messages_numbers(mailbox=mailbox,
                                     tags=[SEEN_FLAG],
                                     inverse=False)

  def get_message(self, number, mailbox="INBOX"):
    """Get the email specified by its number from the specified mailbox.

    Arguments:
      ``number``: The email number to retrieve.
      ``mailbox``: Optional. Optional. The mailbox where to search. Default to ``INBOX``

    Returns:
      ``string``: The string representation of the email.

    Raises:
      ``ScrippyMailError``: When the specified email number does not match any available email.
    """
    try:
      if not self.connected:
        self.connect()
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      typ, data = self.client.fetch(number, '(RFC822)')
      return data[0][1].decode("utf-8")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapFetchError] {err}"
      raise ScrippyMailError(err_msg) from err

  def get_messages(self, mailbox="INBOX", tags=None, inverse=False):
    """Return the list of available emails in the specified mailbox and matching the specified criteria.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

    Returns:
      ``list``: List of string representations of all emails matching specified criteria and mailbox.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    messages = list()
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=inverse)
    for uid in uids:
      messages.append(self.get_message(mailbox=mailbox,
                                       number=uid))
    return messages

  def tag_message(self, number, tags, mailbox="INBOX"):
    """Add one or more tags to the specified email.

    Arguments:
      ``number``: The email number.
      ``tags``: A list of string that will be used as tags to be added to the email.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      logger.debug("Tagging email...")
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      for tag in tags:
        self.client.store(number, "+FLAGS", fr"({tag})")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapTagError] {err}"
      raise ScrippyMailError(err_msg) from err

  def untag_message(self, number, tags, mailbox):
    """Remove one or more tags to the specified email.

    Arguments:
      ``number``: The email number.
      ``tags``: A list of string that will be used as tags to be removed from the email.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      logger.debug("Untagging email...")
      if not self.connected:
        self.connect()
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      for tag in tags:
        self.client.store(number, "-FLAGS", fr"({tag})")
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapTagError] {err}"
      raise ScrippyMailError(err_msg) from err

  def mark_message_as_read(self, number, mailbox="INBOX"):
    """Mark the specified email as 'read'.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    self.tag_message(mailbox=mailbox,
                     number=number,
                     tags=[SEEN_FLAG])

  def mark_message_as_unread(self, number, mailbox="INBOX"):
    """Mark the specified email as 'unread'.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When no available email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    self.untag_message(mailbox=mailbox,
                       number=number,
                       tags=[SEEN_FLAG])

  def tag_messages(self, tags, mailbox="INBOX"):
    """Tag all emails in the specified mailbox with one or more tags.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: A list of string that will be used as tags to be added to each email.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=True)
    for uid in uids:
      self.tag_message(mailbox=mailbox,
                       number=uid,
                       tags=tags)

  def untag_messages(self, mailbox, tags):
    """Remove one or more tags to all emails in the specified mailbox.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: A list of string that will be used as tags to be removed from each email.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags)
    for uid in uids:
      self.untag_message(mailbox=mailbox,
                         number=uid,
                         tags=tags)

  def mark_messages_as_read(self, mailbox="INBOX"):
    """Mark all emails in the specified mailbox as 'read'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    self.tag_messages(mailbox=mailbox,
                      tags=[SEEN_FLAG])

  def mark_messages_as_unread(self, mailbox="INBOX"):
    """Mark all emails in the specified mailbox as 'unread'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    self.untag_messages(mailbox=mailbox,
                        tags=[SEEN_FLAG])

  def delete_message(self, number, mailbox="INBOX"):
    """Delete the specified email in the specified mailbox.

    Arguments:
      ``number``: The email number.
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``

    Raises:
      ``ScrippyMailError``: When no email match the specified number or when the specified mailbox does not match any available mailbox.
    """
    try:
      if not self.connected:
        self.connect()
      logger.debug("Deleting email...")
      if isinstance(number, int):
        number = str(number)
      self.client.select(mailbox=mailbox)
      self.client.store(number, "+FLAGS", DELETE_FLAG)
      self.client.expunge()
    except imaplib.IMAP4.error as err:
      err_msg = f"[ImapDeleteError] {err}"
      raise ScrippyMailError(err_msg) from err

  def delete_messages(self, mailbox="INBOX", tags=None, inverse=False):
    """Delete all emails matching the specified criteria'.

    Arguments:
      ``mailbox``: Optional. The mailbox where to search. Default to ``INBOX``
      ``tags``: Optional. A list of string that will be used to filter emails based on their tags.
      ``inverse``: Boolean. Inverse filter effect when set to ``True``. Default to ``False``.

    Raises:
      ``ScrippyMailError``: When the specified mailbox does not match any available mailbox.
    """
    uids = self.get_messages_numbers(mailbox=mailbox,
                                     tags=tags,
                                     inverse=inverse)
    for uid in sorted(uids, reverse=True):
      self.delete_message(mailbox=mailbox,
                          number=uid)

  def save_message(self, number, filename, mailbox="INBOX"):
    """Save the message identified by the give number to the specified file,

    If the email contains attachments, a directory named after the specified file name and with the ".attachments" extension will be created and all attachments stored into it.

    Arguments:
      ``number``: Int. The number of the email to save.
      ``filename``: String. The complete path to the file where to save the email.
      ``mailbox``: Optional. The directory where to find the email in the mailbox. Default to ``INBOX``

    Returns:
      ``dict``. A two keys dictionary containing the file name where the email has been saved and the list of attachments file names.

      ..  code-block:: python

        {"filename": "/path/to/file",
         "attachments": ["/path/to/file.attachments/attachements_1.txt",
                         "/path/to/file.attachments/attachements_2.txt]}
    """
    logger.debug(f"Saving email to file: {filename}")
    mail = self.get_message(mailbox=mailbox,
                            number=number)
    try:
      return save_email(email_as_string=mail,
                        filename=filename)
    except Exception as err:
      err_msg = f"[ImapFileError] {err.__class__.__name__}: {err}"
      raise ScrippyMailError(err_msg) from err
