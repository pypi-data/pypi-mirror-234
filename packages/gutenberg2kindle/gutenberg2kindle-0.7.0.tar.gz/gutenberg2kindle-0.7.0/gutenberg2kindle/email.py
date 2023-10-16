"""Auxiliary module with functions that help with sending email"""

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from math import ceil
from typing import Final

from gutenberg2kindle.config import (
    SETTINGS_KINDLE_EMAIL,
    SETTINGS_SENDER_EMAIL,
    SETTINGS_SIZE_LIMIT_IN_MB,
    SETTINGS_SMTP_PORT,
    SETTINGS_SMTP_SERVER,
    get_config,
)

EMAIL_SUBJECT: Final[str] = "Your Project Gutenberg ebook!"
EMAIL_BODY: Final[str] = "- Sent with gutenberg2kindle. Happy reading!"


def create_base_email(sender_email: str, kindle_email: str) -> MIMEMultipart:
    """Generates and returns the base email to use when sending a book"""

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = kindle_email
    message["Subject"] = EMAIL_SUBJECT
    message.attach(MIMEText(EMAIL_BODY, "plain"))
    return message


def send_book(book_id: int, book_in_memory: BytesIO, password: str) -> bool:
    """
    Given a book as a file in memory, sends the file via email
    using the stored config if the file is less than the set limit
    """

    # retrieving config
    sender_email = get_config(SETTINGS_SENDER_EMAIL)
    assert isinstance(sender_email, str)

    kindle_email = get_config(SETTINGS_KINDLE_EMAIL)
    assert isinstance(kindle_email, str)

    smtp_server = get_config(SETTINGS_SMTP_SERVER)
    assert isinstance(smtp_server, str)

    port = get_config(SETTINGS_SMTP_PORT)
    assert isinstance(port, int)

    if not is_valid_file_size(book_in_memory):
        return False

    # creating email message
    message = create_base_email(sender_email, kindle_email)

    # loading the file as an attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(book_in_memory.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={book_id}.epub")
    message.attach(part)

    # send email
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, kindle_email, text)

    return True


def is_valid_file_size(book_in_memory: BytesIO) -> bool:
    """
    Given a book as a file in memory, returns whether the file is
    less than the set limit
    """

    # retrieving config
    size_limit = get_config(SETTINGS_SIZE_LIMIT_IN_MB)
    assert isinstance(size_limit, int)

    file_size = bytes_to_mb(len(book_in_memory.getvalue()))
    return file_size <= size_limit


def bytes_to_mb(bytes_: int) -> float:
    """
    Converts bytes to megabytes, rounding up
    to the nearest integer
    """

    return ceil(bytes_ / 1024 / 1024)
