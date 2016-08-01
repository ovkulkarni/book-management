from database import BaseModel
from peewee import *
from playhouse.fields import ManyToManyField

class Book(BaseModel):
	title = CharField(128, verbose_name="Book Title")
	author = CharField(128, verbose_name="Book Author", null=True)
	publisher = CharField(128, verbose_name="Book Publisher", null=True)
	year = DateField(formats=["%Y"], verbose_name="Publishing Year", null=True)
	isbn = CharField(13, verbose_name="Book ISBN", unique=True)
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

	@property
	def total(self):
		_total = 0
		for book in self.books:
			_total += book.price
		return _total
	
