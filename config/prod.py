import os

APP_NAME = "CMWRC Book Store"
APPLICATION_ROOT = "/bookstore"

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(32))

DB_PATH = "/home/bookstore/bookstore.db"

DISPLAY_DEBUG_INFO = False
ENVIRONMENT = "prod"
