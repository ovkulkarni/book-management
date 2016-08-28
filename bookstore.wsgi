import sys, os
sys.path.insert(0, "/home/bookstore/virtualenv/bin/")
os.chdir("/home/bookstore/book-management/")
from app import create_app
create_app("prod").run(port=5000, debug=False)
