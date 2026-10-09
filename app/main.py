import os
import smtplib
from email.message import EmailMessage
from typing import List


def send_shortlist_email(subject: str, body: str, to_email: str, from_email: str, smtp_host: str, smtp_user: str, smtp_password: str, smtp_port: int = 587) -> None:
    if not all([to_email, from_email, smtp_host, smtp_user, smtp_password]):
        print("SMTP settings missing; skipping email send.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
