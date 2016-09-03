#!/usr/bin/env python
from app import create_app
from flask_script import Manager
import database as db

from modules.cart.models import Book, Purchase
from modules.account.models import Account
from modules.inventory.models import Receipt
from modules.account.localutils import hash_password

import importlib

manager = Manager(create_app)
manager.add_option('-e', '--environment', dest='environment', required=True)

@manager.shell
def shell_ctx():
    return dict(db=db)

@manager.command
def create_db():
    """Create tables in the database"""
    tables = [Book, Purchase, Purchase.books.get_through_model(), Account, Receipt]
    for table in tables:
        if table.table_exists():
            print("Table already exists for {}".format(table))
        else:
            table.create_table()
            print("Created table for {}".format(table))

@manager.command
def create_first_user():
    """Create the original user"""
    if not Account.select().where(Account.email == "okulkarni@okulkarni.me").count() > 0:
        a = Account.create(name="Omkar Kulkarni", email="okulkarni@okulkarni.me", password=hash_password("password123"), admin=True)
        a.save()
        print(a)
        return True
    else:
        print("Account already exists!")
        return False

@manager.command
def run_migration(migration):
    """Run a migration"""
    importlib.import_module("migrations.{}".format(migration)).run(db.database)

if __name__ == '__main__':
    manager.run()
