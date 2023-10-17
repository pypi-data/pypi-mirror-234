import os
import email


def save_email(email_as_string, filename):
  attachments = []
  mail = email.message_from_string(email_as_string)
  if mail.get_content_maintype() == 'multipart':
    for part in mail.walk():
      if part.get_content_maintype() != 'multipart' and \
         part.get('Content-Disposition') is not None:
        dir_path = f"{filename}.attachments"
        os.makedirs(dir_path, exist_ok=True)
        part_fname = os.path.basename(part.get_filename())
        attach_fname = os.path.join(dir_path, part_fname)
        with open(attach_fname, mode="wb") as attachment:
          attachment.write(part.get_payload(decode=True))
        attachments.append(attach_fname)
  with open(filename, mode="w", encoding="utf-8") as message:
    message.write(email_as_string)
  return {"filename": filename,
          "attachments": attachments}
