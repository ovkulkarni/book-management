from database import BaseModel
from peewee import *

class Account(BaseModel):
    email = CharField(64, unique=True, verbose_name="Email Address")
    password = CharField(128)
    admin = BooleanField(default=False)
