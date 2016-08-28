activate_this = '/home/bookstore/virtualenv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys, os
sys.path.insert(0, '/home/bookstore/book-management/')
os.chdir("/home/bookstore/book-management/")
from app import create_app
application = create_app("prod")
