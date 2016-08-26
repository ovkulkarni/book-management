import sys, os
sys.path.insert(0, "/var/www/bookstore/virtualenv/bin/")
os.chdir("/var/www/bookstore/book-management/")
from app import create_app
create_app("prod").run(port=5000, debug=False)
