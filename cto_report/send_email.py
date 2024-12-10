import os
from smtplib import SMTP
from email.message import EmailMessage



def send_mail(subject, sender, recipient, body, attachment=None):

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient
    message.set_content(body, subtype="html")

    if attachment:
        with open(attachment, "rb") as f:
            file_data = f.read()
        message.add_attachment(
            file_data, maintype="application", subtype="xlsx", filename=attachment
        )

    server = SMTP()
    server.connect("rb-smtp-bosch2bosch.rbesz01.com")

    server.send_message(message)
