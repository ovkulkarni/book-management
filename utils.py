from flask import flash
from flask_mail import Message
from app import mail
from requests import get
import json
import os


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "{} - {}".format(getattr(form, field).label.text, error), "error")


def isbn_lookup(isbn_number):
    payload = {
        "key": os.getenv("GOOGLE_API_KEY", ""), "q": "isbn:{}".format(isbn_number)}
    r = get("https://www.googleapis.com/books/v1/volumes", params=payload)
    if not r.status_code == 200:
        return None
    try:
        data = json.loads(r.text)["items"][0]["volumeInfo"]
        author = data.get("authors")
        if isinstance(author, list):
            author = ', '.join(author)
        return {
            "title": data.get("title"),
            "author": author
        }
    except KeyError:
        return None


def send_email(from_address, to_addresses, subject, text_body, html_body):
    msg = Message()
    msg.sender = from_address
    msg.recipients = to_addresses
    msg.subject = subject
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
