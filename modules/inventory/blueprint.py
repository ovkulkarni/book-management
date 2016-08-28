from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect, send_from_directory, g
from modules.cart.models import Book, Purchase
from modules.account.models import Account
from .models import Receipt
from .forms import ISBNBookForm, ManualBookForm, SearchForm
from utils import flash_errors
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from os.path import dirname, realpath, isfile, join
from os import getcwd, chdir
from barcode.writer import ImageWriter
from decorators import admin_required, login_required
from database import database
import barcode


inventory = Blueprint("inventory", __name__, template_folder="templates", url_prefix="/inventory")

@inventory.context_processor
def expose_models():
	return dict(Account=Account, Book=Book, int=int)
	
@inventory.route("/")
@admin_required
def view_inventory():
	return render_template("inventory/view_all.html")

@inventory.route("/add/", methods=["GET", "POST"])
@admin_required
def add_to_inventory():
	if not session.get("receipt", None):
		session["receipt"] = []
	form = ISBNBookForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/receipt.html", form=form)
	try:
		b = Book.get(Book.isbn == form.isbn.data)
	except Book.DoesNotExist:
		flash("Book Not In Inventory", "error")
		return redirect(url_for(".add_manually"))
	current_receipts = session.get("receipt", [])
	if not b.serialize() in current_receipts:
		current_receipts.append(b.serialize())
		session["receipt"] = current_receipts
	else:
		flash("Already Recieved This Book", "error")
	return redirect(url_for(".add_to_inventory"))

@inventory.route("/add/manual/", methods=["GET", "POST"])
@admin_required
def add_manually():
	form = ManualBookForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/manual.html", form=form)
	b = Book.create(title=form.title.data, author=form.author.data, publisher=form.publisher.data, year=form.year.data, isbn=form.isbn.data, alt_code=form.alt_code.data, price=form.price.data)
	b.count = 0
	b.save()
	flash("{} added to inventory. Count: {}".format(b.title, b.count), "success")
	return redirect(url_for(".add_to_inventory"))

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
			flash("Invalid User ID", "error")
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
		code = barcode.get('code39', isbn, writer=ImageWriter())
		filename = code.save(isbn)
	chdir(original_path)
	return send_from_directory(barcode_path, "{}.png".format(isbn))

@inventory.route("/search/", methods=["GET", "POST"])
@login_required
def search_for_book():
	all_books = Book.select().order_by(+Book.title)
	form = SearchForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/search.html", form=form, all_books=all_books)
	term = form.query.data
	books = Book.select().where((Book.isbn.contains(term)) | 
								(Book.title.contains(term)) | 
								(Book.alt_code.contains(term)) | 
								(Book.author.contains(term)) )
	return render_template("inventory/results.html", books=books, form=form, all_books=all_books)

@inventory.route("/remove/", methods=["POST"])
@admin_required
def remove_receipt_item():
    current_cart = session.get("receipt", [])
    b = Book.get(Book.isbn == request.form.get("remove_isbn"))
    current_cart.remove(b.serialize())
    session["receipt"] = current_cart
    return redirect(url_for('.add_to_inventory'))

@inventory.route("/clear/")
def clear_receipt():
	session["receipt"] = []
	return redirect(url_for('.add_to_inventory'))

@inventory.route("/complete/", methods=["POST"])
def complete_receipt():
	books = session.get("receipt", [])
	for field in request.form:
		if request.form.get(field, "") == "":
			flash("{} is required".format(field), "error")
			return redirect(url_for(".add_to_inventory"))
	add_books_to_inventory(books, request.form)
	return redirect(url_for('.clear_receipt'))

@database.transaction()
def add_books_to_inventory(books, form):
	for book in books:
		b = Book.get(Book.isbn == book.get("isbn"))
		b.count += int(form.get("quantity-{}".format(b.isbn)))
		r = Receipt.create(book=b, user=g.user, date=datetime.now(), invoice_number=form.get("invoice_number"), 
			invoice_date=datetime.strptime(form.get("invoice_date"), "%Y-%m-%d").date(), unit_price=int(form.get("unit-{}".format(b.isbn))),
			quantity=int(form.get("quantity-{}".format(b.isbn))))
		r.save()
		b.save()
		flash("Received {} - Current Count: {} - Just Added: {}".format(b.title, b.count, r.quantity), "success")
		if r.unit_price > b.price:
			flash("Warning: The Unit Price is greater than the selling price", "warn")




