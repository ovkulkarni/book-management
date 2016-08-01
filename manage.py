from app import create_app
from flask_script import Manager
import database as db

from modules.cart.models import Book, Purchase

manager = Manager(create_app)
manager.add_option('-e', '--environment', dest='environment', required=True)

@manager.shell
def shell_ctx():
    return dict(db=db)

@manager.command
def create_db():
    """Create tables in the database"""
    tables = [Book, Purchase, Purchase.books.get_through_model()]
    for table in tables:
        if table.table_exists():
            print("Table already exists for {}".format(table))
        else:
            table.create_table()
            print("Created table for {}".format(table))

if __name__ == '__main__':
    manager.run()