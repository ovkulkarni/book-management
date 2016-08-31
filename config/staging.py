import os
APP_NAME = "CMWRC Book Store"
SECRET_KEY = "key"
DB_PATH = "/home/bookstore/bookstore-test.db"
DISPLAY_DEBUG_INFO = True
ENVIRONMENT = "Staging"
TEMPLATES_AUTO_RELOAD=True

SEND_ERROR_EMAIL = True
ADMINS = ["okulkarni@okulkarni.me"]
ERROR_EMAIL_SUBJECT = "Bookstore Application Error"

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "bookstoreapplication@chinmayadc.org"
MAIL_PASSWORD = os.getenv("BOOKSTORE_EMAIL_PASSWORD", "")
