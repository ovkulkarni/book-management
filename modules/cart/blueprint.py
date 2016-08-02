from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect
from .models import Book, Purchase
from .forms import AddToCartForm
from utils import flash_errors
from datetime import datetime
from database import database


cart = Blueprint("cart", __name__, template_folder="templates", url_prefix="/cart")

@cart.route("/", methods=["GET", "POST"])
def show_cart():
	if not session.get("cart", None):
		session["cart"] = []
	if not session.get("total", None):
		session["total"] = 0
	form = AddToCartForm(request.form)
	if not form.validate_on_submit():
		flash_errors(form)
		return render_template("cart/cart.html", form=form)
	try:
		b = Book.get(Book.isbn == form.isbn.data)
	except:
		flash("We don't have any books with that ISBN :/", "alert")
		return redirect(url_for('.show_cart'))
	current_cart = session.get("cart", [])
	if current_cart.count(b.serialize()) >= b.count:
		flash("Unable to add - not in stock", "alert")
		return redirect(url_for(".show_cart"))
	current_cart.append(b.serialize())
	session["cart"] = current_cart
	current_total = session.get("total", 0)
	current_total += b.price
	session["total"] = current_total
	flash("Added {} to cart".format(b.title), "success")
	return redirect(url_for('.show_cart'))

@cart.route("/clear/")
def clear_cart():
	session["cart"] = []
	session["total"] = 0
	return redirect(url_for('.show_cart'))

@cart.route("/purchase/", methods=["POST"])
def complete_purchase():
	cart = session.get("cart", [])
	if len(cart) < 1:
		flash("No Books in Cart", "alert")
		return redirect(url_for(".show_cart"))
	for book in cart:
		p = Purchase.create(time=datetime.now())
		b = Book.get(Book.isbn == book.get("isbn"))
		add_book_to_purchase(p, b)
	flash("Completed Purchase and Updated Inventory", "success")
	return redirect(url_for('.clear_cart'))

@database.transaction()
def add_book_to_purchase(purchase, book):
	purchase.books.add(book)
	purchase.total = book.price
	book.count -= 1
	purchase.save()
	book.save()


