from database import BaseModel
from peewee import *
from playhouse.fields import ManyToManyField
from modules.account.models import Account


class Book(BaseModel):
    title = CharField(128, verbose_name="Book Title")
    author = CharField(128, verbose_name="Book Author", null=True)
    publisher = CharField(128, verbose_name="Book Publisher", null=True)
    year = DateField(formats=["%Y"], verbose_name="Publishing Year", null=True)
    isbn = CharField(13, verbose_name="Book ISBN", unique=True)
    alt_code = CharField(10, verbose_name="Alternate Code (SKU)", null=True)
    price = IntegerField(default=7, verbose_name="Book Price")
    count = IntegerField(default=0, verbose_name="Book Count")

    def serialize(self):
        return {
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "year": self.year,
            "isbn": self.isbn,
            "price": self.price,
            "count": self.count
        }


class Purchase(BaseModel):
    time = DateTimeField(verbose_name="Purchase Date/Time")
    books = ManyToManyField(Book, related_name="purchases")
    seller = ForeignKeyField(Account)
    method = CharField(7, verbose_name="Sale Type")
    comment = CharField(128, verbose_name="Sale Comment")
    total = IntegerField("Purchase Total")

    @property
    def book(self):
        if len(self.books) == 1:
            return self.books[0]
        elif len(self.books) == 0:
            return "[deleted]"
        else:
            raise IntegrityError("Purchase Should Only Have 1 Book")
