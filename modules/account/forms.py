from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, validators

class LoginForm(Form):
	email = StringField("Email Address", [validators.DataRequired(), validators.Email()])
	password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=92)])

class CreateAccountForm(Form):
	email = StringField("Email Address", [validators.DataRequired(), validators.Email()])
	password = PasswordField("Password", [validators.DataRequired(), validators.Length(min=8, max=92), 
		validators.EqualTo('confirm', message="Passwords must match!")])
	confirm = PasswordField('Confirm password')
	admin = BooleanField("Admin Account")

class ChangeEmailForm(Form):
	email = StringField("Email Address", [validators.DataRequired(), validators.Email()])