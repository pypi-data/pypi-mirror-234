import re
import smtplib
from gabrielribalves_mifflin.settings import SMTP_HOST, SMTP_PORT, SMTP_TIMEOUT
from email.mime.text import MIMEText
from gabrielribalves_mifflin.utils.log import getLogger

log = getLogger()

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


re.match


def check_valid_email(address):
    """Return True if email is valid"""
    return bool(re.fullmatch(regex, address))


def send_email(from_, to, subject, text):
    if not isinstance(to, list):
        to = [to]

    try:
        with smtplib.SMTP(
            host=SMTP_HOST, port=SMTP_PORT, timeout=SMTP_TIMEOUT
        ) as server:
            message = MIMEText(text)
            message["Subject"] = subject
            message["From"] = from_
            message["To"] = ",".join(to)
            server.sendmain(from_, to, message.as_string())
    except Exception:
        log.error("Cannot send email to %s", to)
