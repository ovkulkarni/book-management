from database import BaseModel
from peewee import *
from modules.account.models import Account
from modules.cart.models import Book

class Receipt(BaseModel):
    book = ForeignKeyField(Book, related_name="receipts")
    user = ForeignKeyField(Account, related_name="additions")
    date = DateTimeField(verbose_name="Receipt Date/Time")
    invoice_number = CharField(64, verbose_name="Invoice Number")
    invoice_date = DateField(formats=["%Y-%m-%d"], verbose_name="Invoice Date")
    quantity = IntegerField(verbose_name="Quantity Added")
    unit_price = IntegerField(verbose_name="Unit Price")