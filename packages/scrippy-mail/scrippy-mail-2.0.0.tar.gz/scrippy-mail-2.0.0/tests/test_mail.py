"""Test scrippy_mail."""
import os
from scrippy_mail import ScrippyMailError, logger
from scrippy_mail.smtp import Client as SmtpClient
from scrippy_mail.pop import Client as PopClient
from scrippy_mail.imap import Client as ImapClient


MAIL_HOST = "mailer"
MAIL_SMTP_PORT = 2500
MAIL_POP_PORT = 110
MAIL_IMAP_PORT = 143
MAIL_TLS = False
MAIL_SSL = False
MAIL_FROM = "luiggi.vercotti@flying.circus"
MAIL_TO = "harry.fink@flying.circus"
MAIL_PASSWORD = "0123456789"
MAIL_BOX = "INBOX"
MAIL_FILE = "/tmp/message.txt"
MAIL_SUBJECT = "Rapport d'erreur"
MAIL_BODY = """Bonjour Harry Fink
Vous recevez cet e-mail car vous faites partie des administrateurs fonctionnels de l'application Dead Parrot.

L'execution du script s'est terminee avec l'erreur suivante:
- It's not pinin'! It's passed on! This parrot is no more!

--
Cordialement.
Luiggi Vercotti
"""


def test_send_mail():
  """Test envoi de mail."""
  with SmtpClient(host=MAIL_HOST,
                  port=MAIL_SMTP_PORT,
                  starttls=MAIL_TLS,
                  exit_on_error=True) as smtp_client:
    recipients = [MAIL_TO]
    try:
      smtp_client.send(subject=MAIL_SUBJECT, body=MAIL_BODY, sender=MAIL_FROM,
                       recipients=recipients, cc=None, bcc=None,
                       attachments=None)
      logger.info(f"Mail successfully sent to {MAIL_TO}")
    except ScrippyMailError as err:
      logger.error(err)
      raise err


def test_imap():
  mail_user = "harry.fink@flying.circus"
  expected_content = "It's not pinin'! It's passed on! This parrot is no more!"
  with ImapClient(host=MAIL_HOST,
                  port=MAIL_IMAP_PORT,
                  username=mail_user,
                  password=MAIL_PASSWORD,
                  starttls=MAIL_TLS) as imap_client:
    assert imap_client.get_unread_messages_numbers(mailbox=MAIL_BOX) == [b'1']
    message = imap_client.get_message(number=1,
                                      mailbox=MAIL_BOX)
    assert expected_content in message
    imap_client.mark_message_as_read(number=1,
                                     mailbox=MAIL_BOX)
    assert imap_client.get_unread_messages_numbers(mailbox=MAIL_BOX) == list()
    imap_client.mark_message_as_unread(number=1,
                                       mailbox=MAIL_BOX)
    assert imap_client.get_unread_messages_numbers(mailbox=MAIL_BOX) == [b'1']
    imap_client.save_message(number=1,
                             filename=MAIL_FILE, mailbox=MAIL_BOX)
    assert os.path.isfile(MAIL_FILE)
    imap_client.delete_message(number=1,
                               mailbox=MAIL_BOX)
    try:
      imap_client.get_message(number=1,
                              mailbox=MAIL_BOX)
      raise Exception("Missed: ImapClient.delete_message")
    except ScrippyMailError:
      pass


def test_pop_mail():
  test_send_mail()
  mail_user = "harry.fink@flying.circus"
  expected_content = "It's not pinin'! It's passed on! This parrot is no more!"
  with PopClient(host=MAIL_HOST,
                 port=MAIL_POP_PORT,
                 username=mail_user,
                 password=MAIL_PASSWORD,
                 starttls=MAIL_TLS) as pop_client:
    assert pop_client.get_message_count() == 1
    for number in pop_client.get_messages_numbers():
      assert expected_content in pop_client.get_message(number=number)
      pop_client.save_message(number=number, filename=MAIL_FILE)
      assert os.path.isfile(MAIL_FILE)
      pop_client.delete_message(number=number)
    try:
      pop_client.get_message(number=1)
      raise Exception("Missed: PopClient.delete_message")
    except ScrippyMailError:
      pass
