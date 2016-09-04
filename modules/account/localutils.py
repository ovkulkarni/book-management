from passlib.apps import custom_app_context as password_context
from flask import session
from .models import Account


def hash_password(plain, admin=False):
    if not admin:
        return password_context.encrypt(plain)
    else:
        return password_context.encrypt(plain, category="admin")


def verify_password(plain, account):
    return password_context.verify(plain, account.password)


def get_current_user():
    if "uid" in session and session["logged_in"]:
        return Account.get(Account.id == session["uid"])
    return None
