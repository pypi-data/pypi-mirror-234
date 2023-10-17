
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-mail/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-mail.png "Scrippy, my scrangourou friend")

# `scrippy_mail`

SMTP, POP3 and IMAP clients for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Prerequisites

### Python Modules

#### Required Modules list

- None

## Installation

### With `pip`

```bash
pip install scrippy-mail
```

### Manual

```bash
git clone https://codeberg.org/scrippy/scrippy-mail.git
cd scrippy-mail
python -m pip install -r requirements.txt
make install
```

### `scrippy_mail`

The `scrippy_mail` module offers the following clients objects for sending and retrieving emails:
- `scrippy_mail.smtp.client` for sending email using *SMTP* protocol
- `scrippy_mail.imap.client` for email retrieval using *IMAP* protocol
- `scrippy_mail.pop.client` for email retrieval using *POP3* protocol

Each client are able to connect to remote server using secure connection with *SSL* or *STARTTLS*.

The `scrippy_mail.mail` module offers a simplified interface for sending emails via the `Mailer` object.

Each client use the same following parameter set:
- `host`: The name of the mail server to use (default: localhost)
- `port`: The port number to contact the mail server (default: 25)
- `username`: The username to authenticate on the mail server
- `password`: The password to authenticate on the mail server
- `ssl`: A boolean indicating whether to use SSL (default: False)
- `starttls`: A boolean indicating whether to use STARTTLS (default: False)
- `ssl_verify`: A boolean indicating whether to verify remote server *SSL* certificate (default: `True`)
- `timeout`: An integer indicating the maximum delay in seconds to succeed in a connection (default: 60)
- `exit_on_error`: A boolean. If set to `False`, any error encountered will be logged as a warning. When set to `True`, exit the workflow if any error is encountered (Default: `True`)

**NOTE:**
- `ssl` and `starttls` are mutualy exclusive. Using both at the same time raises an error.
- In doubt use `ssl` for maximum secure connection.

#### Sending Mail

**NOTE:**
- Recipients, Cc or BCc addresses must be provided as lists.
- Each email address must be an email address that complies with [RFC 5322](https://tools.ietf.org/html/rfc5322.html).
- Attachments must be a list of file path


```python
from scrippy_mail import ScrippyMailError, logger
from scrippy_mail.smtp import client as SmtpClient

mail_username = "luiggi.vercotti@flying.circus"
mail_password = "D3ADP4ARR0T"
mail_host = "smtp.flying.circus"
mail_port = "465"
mail_ssl = True
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

with SmtpClient(host=mail_host,
                port=mail_port,
                username=mail_user,
                password=mail_password,
                ssl=mail_ssl) as smtp_client:
  recipients = [mail_to]
  try:
    smtp_client.send(subject=mail_subject, body=mail_body, sender=mail_from,
                     recipients=recipients, cc=None, bcc=None, attachments=None,
                     exit_on_error=True)
    logger.info(f"Mail successfully sent to {mail_to}")
  except ScrippyMailError as err:
    logger.error(err)
    raise err
```

#### *IMAP* operations

The *IMAP* client allows all operations expected from an *IMAP* client such as but not limited to:
- Get unread messages
- Mark message as read/unread
- Delete messages
- Save a message in a local filesystem


```python
from scrippy_mail import ScrippyMailError, logger
from scrippy_mail.imap import client as ImapClient

mail_user = "luiggi.vercotti@flying.circus"
mail_password = "D3ADP4ARR0T"
mail_host = "imap.flying.circus"
mail_port = "993"
mail_tls = True
mail_box = "INBOX"
mail_file = "/tmp/message.txt"

with ImapClient(host=mail_host,
                port=mail_port,
                username=mail_user,
                password=mail_password,
                starttls=mail_tls) as imap_client:
  try:
    for number in imap_client.get_unread_messages_numbers(mailbox=mail_box):
      message = imap_client.get_message(number=number, mailbox=mail_box)
      # log message:
      logger.info(message)
      # Mark message as read
      imap_client.mark_message_as_read(number=number, mailbox=mail_box)
      # Mark message as unread
      imap_client.mark_message_as_unread(number=number, mailbox=mail_box)
      # Save message (attachments will be saved in a directory netx to the message)
      imap_client.save_message(number=number, filename=mail_file, mailbox=mail_box)
      # Delete message
      imap_client.delete_message(number=number, mailbox=mail_box)
  except ScrippyMailError as err:
    logger.error(err)
    raise err
```


#### POP3 operations

The *POP3* client allows all operations expected from an *POP3* client such as but not limited to:
- Get messages
- Delete messages
- Save a message in a local filesystem

**NOTE:** The **POP3** protocol does not manage message states as *read* or *unread*. This feature is only avalaible with *IMAP*.


```python
from scrippy_mail import ScrippyMailError, logger
from scrippy_mail.pop import client as PopClient

mail_user = "luiggi.vercotti@flying.circus"
mail_password = "D3ADP4ARR0T"
mail_host = "imap.flying.circus"
mail_port = "995"
mail_ssl = True
mail_box = "INBOX"
mail_file = "/tmp/message.txt"

with PopClient(host=mail_host,
                port=mail_port,
                username=mail_user,
                password=mail_password,
                ssl=mail_ssl) as pop_client:
  try:
    # Get message count
    count = pop_client.get_message_count()
    logger.info(f"{count} messages are available in this mailbox.")
    # Get all available messages and work on each of them
    for number in pop_client.get_messages_numbers():
      message = pop_client.get_message(number=number)
      # log message:
      logger.info(message)
      # Save message (attachments will be saved in a directory netx to the message)
      pop_client.save_message(number=number, filename=mail_file)
      # Delete message
      pop_client.delete_message(number=number)
  except ScrippyMailError as err:
    logger.error(err)
    raise err
```

Convenient wrapper methods:
- `PopClient.get_all_messages()`: Returns all mesasges in a list
- `PopClient.delete_all_messages()`: Deletes all messages
