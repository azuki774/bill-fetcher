import smtplib, ssl
from email.mime.text import MIMEText

import logging
import json
import os
from pythonjsonlogger import jsonlogger

lg = logging.getLogger(__name__)
lg.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.DEBUG)
json_fmt = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s", json_ensure_ascii=False
)
h.setFormatter(json_fmt)
lg.addHandler(h)


notify_address = os.getnev("notify_address")
gmail_account = os.getnev("mail_user")
gmail_password = os.getnev("mail_pass")


def make_mime_text(mail_to, subject, body):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account
    return msg


def send_gmail(msg):
    server = smtplib.SMTP_SSL(
        "smtp.gmail.com", 465, context=ssl.create_default_context()
    )
    server.set_debuglevel(0)
    server.login(gmail_account, gmail_password)
    server.send_message(msg)


def send_alert_main(body):
    lg.info("send alert mail")
    joblabel = os.getenv("job_label")
    msg = make_mime_text(
        mail_to=notify_address,
        subject="job: {0}: 取得に失敗しました".format(joblabel),
        body=body,
    )
    send_gmail(msg)
