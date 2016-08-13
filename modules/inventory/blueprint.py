from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect, send_from_directory
from modules.cart.models import Book, Purchase
from modules.account.models import Account
from .forms import ISBNBookForm, ManualBookForm, SearchForm
from utils import flash_errors, isbn_lookup
from datetime import date
from dateutil.relativedelta import relativedelta
from os.path import dirname, realpath, isfile, join
from os import getcwd, chdir
from barcode.writer import ImageWriter
from decorators import admin_required, login_required
import barcode


inventory = Blueprint("inventory", __name__, template_folder="templates", url_prefix="/inventory")

@inventory.context_processor
def expose_models():
	return dict(Account=Account, int=int)
	
@inventory.route("/")
@admin_required
def view_inventory():
	return render_template("inventory/view_all.html")

@inventory.route("/add/", methods=["GET", "POST"])
@admin_required
def add_to_inventory():
	form = ISBNBookForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/add.html", form=form)
	try:
		b = Book.get(Book.isbn == form.isbn.data)
	except Book.DoesNotExist:
		data = isbn_lookup(form.isbn.data)
		if not data:
			flash("Invalid ISBN", "alert")
			return redirect(url_for(".add_manually"))
		if len(data.get("authors", [])) > 0:
			author = ', '.join(data.get("authors"))
		else:
			author = "Unknown"
		if not form.price.data:
			flash("Please Enter a Price", "alert")
			return redirect(url_for(".add_to_inventory"))
		b = Book.create(title=data.get("title"), author=author, publisher=data.get("publisher"), year=data.get("publishedDate", "").split("-")[0], isbn=form.isbn.data, price=form.price.data)
	b.count += int(form.quantity.data)
	b.save()
	flash("{} added to inventory. Count: {}".format(b.title, b.count), "success")
	return redirect(url_for(".add_to_inventory"))

@inventory.route("/add/manual/", methods=["GET", "POST"])
@admin_required
def add_manually():
	form = ManualBookForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/manual.html", form=form)
	b = Book.create(title=form.title.data, author=form.author.data, publisher=form.publisher.data, year=form.year.data, isbn=form.isbn.data, alt_code=form.alt_code.data, price=form.price.data)
	b.count += 1
	b.save()
	flash("{} added to inventory. Count: {}".format(b.title, b.count), "success")
	return redirect(url_for(".view_inventory"))

@inventory.route("/edit/<isbn>/", methods=["GET", "POST"])
@admin_required
def edit_book(isbn):
	b = Book.get(Book.isbn == isbn)
	form = ManualBookForm(request.form, b)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/manual.html", form=form)
	b.title = form.title.data
	b.author = form.author.data
	b.publisher = form.publisher.data
	b.year = form.year.data
	b.isbn = form.isbn.data
	b.alt_code = form.alt_code.data
	b.price = form.price.data
	b.save()
	flash("Updated {}".format(b.title), "success")
	return redirect(url_for(".view_inventory"))

@inventory.route("/purchases/")
@admin_required
def view_purchases():
	if request.args.get("time", None):
		time = request.args.get("time", "month")
		one_year_ago = date.today() - relativedelta(years=1)
		one_month_ago = date.today() - relativedelta(months=1)
		one_week_ago = date.today() - relativedelta(weeks=1)
		if time == "year":
			purchases = Purchase.select().where(Purchase.time > one_year_ago).order_by(Purchase.time.desc())
		elif time == "week":
			purchases = Purchase.select().where(Purchase.time > one_week_ago).order_by(Purchase.time.desc())
		elif time == "today":
			purchases = Purchase.select().where(Purchase.time > date.today()).order_by(Purchase.time.desc())
		else:
			purchases = Purchase.select().where(Purchase.time > one_month_ago).order_by(Purchase.time.desc())
	elif request.args.get("user_id", None):
		user_id = int(request.args.get("user_id"))
		try:
			a = Account.get(Account.id == user_id)
			flash("Showing purchases created by {}".format(a.name), "success")
			purchases = Purchase.select().where(Purchase.seller == a).order_by(Purchase.time.desc())
		except Account.DoesNotExist:
			flash("Invalid User ID", "alert")
			return redirect(url_for('.view_purchases'))
	else:
		purchases = Purchase.select().order_by(Purchase.time.desc())
	total_money = 0
	for purchase in purchases:
		total_money += purchase.total
	return render_template("inventory/purchases.html", purchases=purchases, total=total_money)

@inventory.route("/barcode/<isbn>/")
@admin_required
def generate_barcode(isbn):
	original_path = getcwd()
	current_path = dirname(realpath(__file__))
	barcode_path = join(current_path, "static/barcodes")
	chdir(barcode_path)
	if not isfile(join(barcode_path, "{}.png".format(isbn))):
		code = barcode.get('isbn13', isbn, writer=ImageWriter())
		filename = code.save(isbn)
	chdir(original_path)
	return send_from_directory(barcode_path, "{}.png".format(isbn))

@inventory.route("/search/", methods=["GET", "POST"])
@login_required
def search_for_book():
	form = SearchForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/search.html", form=form)
	term = form.query.data
	books = Book.select().where((Book.isbn.contains(term)) | 
								(Book.title.contains(term)) | 
								(Book.alt_code.contains(term)) | 
								(Book.author.contains(term)) )
	return render_template("inventory/results.html", books=books, form=form)



