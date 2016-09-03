from database import BaseModel
from peewee import *

class Account(BaseModel):
    name = CharField(64, verbose_name="Full Name")
    email = CharField(64, unique=True, verbose_name="Email Address")
    password = CharField(128)
    admin = BooleanField(default=False)
    disabled = BooleanField(default=False)
