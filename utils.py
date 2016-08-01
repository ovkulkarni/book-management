from flask import flash
from requests import get
import json
import os

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("{} - {}".format(getattr(form, field).label.text, error), "alert")

def isbn_lookup(isbn_number):
	payload = {"key": os.getenv("GOOGLE_API_KEY", ""), "q": "isbn:{}".format(isbn_number)}
	r = get("https://www.googleapis.com/books/v1/volumes", params=payload)
	if not r.status_code == 200:
		return None
	try:
		return json.loads(r.text)["items"][0]["volumeInfo"]
	except KeyError:
		return None