# # -*- coding: utf-8 -*-

import io
import os
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

"""
Envia un correo automático utilizando un App Password ded Google
https://towardsdatascience.com/automate-sending-emails-with-gmail-in-python-449cc0c3c317
"""


class EmailSender(object):
    def __init__(self):
        self.SERVER: str = None
        self.PORT: int = None
        self.FROM: str = None
        self.PASS: str = None
        self.TO: str = None
        self.SUBJECT: str = None
        self.HTML: str = None
        self.FILES: list[str] = []
        self.FOOTER: str = None
        self.prepare_footer()

    def configure_server(self, SERVER: str, PORT: int, FROM: str, PASS: str):
        self.FROM = FROM
        self.PASS = PASS
        self.SERVER = SERVER
        self.PORT = PORT

    def send_email(
        self, to: str, subject: str, message: str, files: List = None, streams: List[Dict] = None
    ):
        msg = MIMEMultipart()
        if to is not None:
            self.TO = to
        if subject is not None:
            self.SUBJECT = subject
        msg["From"] = self.FROM
        msg["To"] = self.TO
        msg["Subject"] = Header(self.SUBJECT)

        self.HTML = message

        if self.HTML:
            msg.attach(MIMEText(self.HTML, "html"))

        msg.attach(MIMEText(self.FOOTER, "html"))

        if files is not None and len(files):
            self.prepare_files(files)

        for f in self.FILES:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                'attachment; filename="{0}"'.format(os.path.basename(f)),
            )
            msg.attach(part)

        if streams is not None and len(streams):
            for f in streams:
                attach: io.StringIO = f["attachment"]
                if type(attach) is io.StringIO:
                    attachment = MIMEText(attach.getvalue())
                    attachment.add_header(
                        "Content-Disposition", "attachment", filename=f["filename"] or "out"
                    )
                    msg.attach(attachment)

        # image_path = f"{os.getcwd()}\\lib\\utils\\logo.png"

        # fp = open(image_path, 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()

        # # Define the image's ID as referenced above
        # msgImage.add_header('Content-ID', '<image1>')
        # msg.attach(msgImage)

        s = smtplib.SMTP(self.SERVER, self.PORT)
        s.ehlo()  # Hostname to send for this command defaults to the fully qualified domain name of the local host.
        s.starttls()  # Puts connection to SMTP server in TLS mode
        s.login(self.FROM, self.PASS)
        s.sendmail(self.FROM, self.TO.split(","), msg.as_string())
        s.quit()

    def prepare_footer(self):
        self.FOOTER = (
            "<br/><br/>"
            + "<p>This email was sent automatically</p>"
            +
            # "<img src=\"cid:image1\" alt=\"Logo\" style=\"height:70px;\"><br/>"
            '<p><a href="https://ai/">VTarget</a></p>'
        )

    def prepare_files(self, files=[]):
        self.FILES = list(filter(lambda x: os.path.exists(x), files))


# if __name__ == "__main__":
#     se = EmailSender()
#     se.send_email()
