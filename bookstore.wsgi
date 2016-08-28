import sys, os
sys.path.insert(0, "/home/bookstore/virtualenv/bin/")
os.chdir("/home/bookstore/book-management/")
from app import create_app
application = create_app("prod")
