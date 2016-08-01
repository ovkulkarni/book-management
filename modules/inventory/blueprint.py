from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect
from modules.cart.models import Book
from .forms import ISBNBookForm, ManualBookForm
from utils import flash_errors, isbn_lookup


inventory = Blueprint("inventory", __name__, template_folder="templates", url_prefix="/inventory")

@inventory.route("/")
def view_inventory():
	books = Book.select().order_by(+Book.id)
	return render_template("inventory/view_all.html", books=books)

@inventory.route("/add/", methods=["GET", "POST"])
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
		if len(data["authors"]) > 0:
			author = data["authors"][0]
		else:
			author = None
		if not form.price.data:
			flash("Please Enter a Price", "alert")
			return redirect(url_for(".add_to_inventory"))
		b = Book.create(title=data.get("title"), author=author, publisher=data.get("publisher"), year=data.get("publishedDate", "").split("-")[0], isbn=form.isbn.data, price=form.price.data)
	b.count += 1
	b.save()
	flash("{} added to inventory. Count: {}".format(b.title, b.count), "success")
	return redirect(url_for(".view_inventory"))

@inventory.route("/add/manual/", methods=["GET", "POST"])
def add_manually():
	form = ManualBookForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("inventory/manual.html", form=form)
	b = Book.create(title=form.title.data, author=form.author.data, publisher=form.publisher.data, year=form.year.data, isbn=form.isbn.data, price=form.price.data)
	b.count += 1
	b.save()
	flash("{} added to inventory. Count: {}".format(b.title, b.count), "success")
	return redirect(url_for(".view_inventory"))

@inventory.route("/edit/<isbn>/", methods=["GET", "POST"])
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
	b.price = form.price.data
	b.save()
	flash("Updated {}".format(b.title))
	return redirect(url_for(".view_inventory"))
