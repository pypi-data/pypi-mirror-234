
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-mail/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-mail.png "Scrippy, my scrangourou friend")

# `scrippy_mail`

SMTP, POP3 and SpamAssassin client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python Modules

#### Required Modules list

- None

## Installation

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-mail.git
cd scrippy-mail
python -m pip install -r requirements.txt
make install
```

### With `pip`

```bash
pip install scrippy-mail
```

### Usage

### `scrippy_mail`

The `scrippy_mail.mail` module offers a simplified interface for sending emails via the `Mailer` object.

This module also offers an interface to `SpamAssassin` via the `SpamAssassinClient` object and a `POP3` interface via the `PopClient` object.

These last two interfaces are not fully documented and do not implement all the protocols they are supposed to support. However, they can be used in production for limited needs.

The source code of the `scrippy_mail.mail.popclient` and `scrippy_mail.mail.spamassassin` modules and the comments it contains remains the best source of documentation. [`Use the Source, Luke`](https://en.wiktionary.org/wiki/UTSL).

The following parameters are optional when instanciating a `scrippy_mail.mail.Mailer` object:
- `host`: The name of the mail server to use (default: localhost)
- `port`: The port number to contact the mail server (default: 25)
- `user`: The username to authenticate on the mail server
- `password`: The password to authenticate on the mail server
- `starttls`: A boolean indicating whether to use STARTTLS (default: False)
- `timeout`: An integer indicating the maximum delay in seconds to succeed in a connection (default: 60)

#### Sending Mail

The `Mailer.send()` method for sending the message accepts the following 4 required arguments:
- `subject`: A string used as the email subject
- `body`: A string used as the email body
- `to_addrs`: A *tuple* containing the list of destination email addresses
- `from_addr`: The email address of the sender

If the `to_addrs` argument is not a *tuple*, it will be converted as such. Typically if the email has only one recipient, passing the single email address of that recipient as a string will be sufficient.

If the email needs to be sent to multiple recipients, the destination addresses must be provided as a *tuple*.

Each email address must be an email address that complies with [RFC 5322](https://tools.ietf.org/html/rfc5322.html).

The `Mailer.send()` method returns `True` on success and `False` on email send failure.

```python
from scrippy_mail import mail

mail_host = "smtp.flying.circus"
mail_port = "465"
mail_tls = True
mail_from = "luigi.vercotti@flying.circus"
mail_to = "harry.fink@flying.circus"
mail_subject = "Error report"
mail_body = """Dear Harry Fink,

You receive this email because you are one of the functional administrators of the Dead Parrot application.

The script execution ended with the following error:
- It's not pinin’! It's passed on! This parrot is no more!

--
Kind regards,
Luiggi Vercotti
"""

mailer = mail.Mailer(host=mail_host, port=mail_port, starttls=mail_tls)
to_addrs = (mail_to,)

if mailer.send(subject, body, to_addrs, mail_from):
  logging.debug("Email successfully sent")
```

#### Retrieving Mail (POP3)

The `PopClient` client allows to query a _POP3_ server. This very basic client does not handle _TLS_ encrypted connections.

```python
import email
from scrippy_mail import mail

mail_host = "smtp.flying.circus"
mail_port = "110"
mail_account = "luigi.vercotti@flying.circus"
mail_password = "D3ADP4ARR0T"

client = mail.PopClient(host=mail_host, port=mail_port, timeout=5)
client.connect()
client.authenticate(mail_account, mail_password)
# Get number of available mails
# client.stat() returns raw data, it's up to the developer to
# process it to be able to use it.
num_mails = client.stat()
# Get the latest mail
mail_content = client.retr(1)
# Get the content (Body)
mail_content = email.message_from_bytes(mail_content).get_payload()
mail_content = mail_content.replace("=\r\n", "")
mail_content = mail_content.replace("\r\n.\r\n", "\n")
mail_content = "\n".join(mail_content.split("\r\n"))
# Delete the latest mail
client.dele(1)
client.bye()
```
