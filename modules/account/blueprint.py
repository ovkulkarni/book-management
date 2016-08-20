from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect, send_from_directory, g
from .models import Account
from .forms import LoginForm, CreateAccountForm, ChangeEmailForm
from utils import flash_errors
from .localutils import hash_password, verify_password, get_current_user
from decorators import admin_required, login_required

account = Blueprint("account", __name__, template_folder="templates", url_prefix="/account")

@account.route("/", methods=["GET", "POST"])
@login_required
def info():
	form = ChangeEmailForm(request.form, g.user)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("account/info.html", form=form)
	g.user.email = form.email.data
	g.user.name = form.name.data
	g.user.save()
	flash("Updated Info", "success")
	return redirect(url_for('.info'))

@account.route("/change_password/", methods=["GET", "POST"])
@login_required
def change_password():
	if request.method == "POST":
		if not verify_password(str(request.form.get("original_password", "")), g.user):
			flash("Invalid Credentials", "error")
			return redirect(url_for('.change_password'))
		if not request.form.get("new_password", "a") == request.form.get("confirm_new_password", "b"):
			flash("Passwords must match!", "error")
			return redirect(url_for('.change_password'))
		if not len(request.form.get("new_password", "a")) > 7 and len(request.form.get("new_password")) < 92:
			flash("Password must be between 8 and 92 characters long!", "error")
			return redirect(url_for('.change_password'))
		g.user.password = hash_password(request.form.get("new_password"))
		g.user.save()
		flash("Updated Password", "success")
		return redirect(url_for('.info'))
	return render_template("account/change.html")

@account.route("/add/", methods=["GET", "POST"])
@admin_required
def add_account():
	form = CreateAccountForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("account/create.html", form=form)
	if not request.form.get("admin", None):
		admin_account = False
	else:
		admin_account = True
	matching_emails = Account.select().where(Account.email == form.email.data)
	if matching_emails.count() > 0:
		flash("An account already exists with that email.", "error")
		return redirect(url_for('.add_account'))
	a = Account.create(name=form.name.data, email=form.email.data, password=hash_password(form.password.data), admin=admin_account)
	a.save()
	flash("Account Created", "success")
	return redirect(url_for('.add_account'))

@account.route("/login/", methods=["GET", "POST"])
def login():
	form = LoginForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("account/login.html", form=form)
	accounts = Account.select().where(Account.email == form.email.data)
	if not accounts.count() > 0:
		flash("Invalid Credentials", "error")
		return redirect(url_for('.login'))
	if not verify_password(form.password.data, accounts[0]):
		flash("Invalid Credentials", "error")
		return redirect(url_for('.login'))
	session["uid"] = accounts[0].id
	session["logged_in"] = True
	flash("Successfully Logged In", "success")
	return redirect(request.args.get("next", url_for('cart.show_cart')))

@account.route("/logout/")
@login_required
def logout():
	session["uid"] = -1
	session["logged_in"] = False
	flash("Successfully Logged Out", "success")
	return redirect(url_for('home_page'))


@account.before_app_request
def set_user():
    g.user = get_current_user()
