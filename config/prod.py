import os

APP_NAME = "CMWRC Book Store"

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))

DB_PATH = "/home/bookstore/bookstore.db"

DISPLAY_DEBUG_INFO = False
ENVIRONMENT = "prod"

SEND_ERROR_EMAIL = True
ADMINS = ["okulkarni@okulkarni.me"]
APP_FROM_EMAIL = "bookstoreapplication@chinmayadc.org"
ERROR_EMAIL_SUBJECT = "Bookstore Application Error"
