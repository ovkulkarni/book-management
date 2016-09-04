from flask_wtf import Form
from wtforms import StringField, IntegerField, DateField, FileField, validators


class AddToCartForm(Form):
    isbn = StringField("ISBN Number", [validators.DataRequired(),
                                       validators.Regexp(r'((978|979)\d{10}|999\d{3})', message="Please enter a valid ISBN Number.")])
