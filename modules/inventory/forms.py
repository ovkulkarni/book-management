from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, validators

class ISBNBookForm(Form):
	isbn = StringField("ISBN Number", [validators.DataRequired(), 
		validators.Regexp(r'(978|979)\d{10}', message="Please enter a valid 13-digit ISBN Number.")])
	price = IntegerField("Book Price", [validators.Optional()])

class ManualBookForm(Form):
	title = StringField("Book Title", [validators.DataRequired(), validators.Length(max=128)])
	author = StringField("Book Author", [validators.Optional(), validators.Length(max=128)])
	publisher = StringField("Book Publisher", [validators.Optional(), validators.Length(max=128)])
	year = StringField("Publishing Year", [validators.Optional()])
	isbn = StringField("ISBN Number", [validators.DataRequired(), 
		validators.Regexp(r'(978|979)\d{10}', message="Please enter a valid 13-digit ISBN Number.")])
	price = IntegerField("Book Price", [validators.Optional()])
