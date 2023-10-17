"""Test scrippy_mail."""
import email
from scrippy_mail import mail

MAIL_HOST = "mailer"
MAIL_SMTP_PORT = 2500
MAIL_POP_PORT = 110
MAIL_TLS = False
MAIL_SSL = False
MAIL_FROM = "luiggi.vercotti@flying.circus"
MAIL_TO = "harry.fink@flying.circus"
MAIL_PASSWORD = "0123456789"
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
  mailer = mail.Mailer(host=MAIL_HOST, port=MAIL_SMTP_PORT, starttls=MAIL_TLS)
  to_addrs = (MAIL_TO,)
  assert mailer.send(MAIL_SUBJECT, MAIL_BODY, to_addrs, MAIL_FROM)


def test_pop_mail():
  """Test récupération de mail."""
  client = mail.PopClient(host=MAIL_HOST, port=MAIL_POP_PORT, timeout=5)
  client.connect()
  client.authenticate(MAIL_TO, MAIL_PASSWORD)
  num_mails = client.stat()
  mail_content = client.retr(1)
  check_response(num_mails, mail_content)
  client.dele(1)
  client.bye()


def check_response(num_mails, mail_content):
  assert num_mails[0:6].decode() == "+OK 1 "
  mail_content = email.message_from_bytes(mail_content).get_payload()
  mail_content = mail_content.replace("=\r\n", "")
  mail_content = mail_content.replace("\r\n.\r\n", "\n")
  mail_content = "\n".join(mail_content.split("\r\n"))
  assert mail_content == MAIL_BODY
