import os

APP_NAME = "CMWRC Book Store"

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))

DB_PATH = "/home/bookstore/bookstore.db"

DISPLAY_DEBUG_INFO = False
ENVIRONMENT = "Production"

SEND_ERROR_EMAIL = True
ADMINS = ["okulkarni@okulkarni.me"]
ERROR_EMAIL_SUBJECT = "Bookstore Application Error"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "{} <bookstoreapplication@chinmayadc.org>".format(APP_NAME)
MAIL_PASSWORD = os.getenv("BOOKSTORE_EMAIL_PASSWORD", "")
