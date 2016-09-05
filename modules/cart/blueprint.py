from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect, g
from .models import Book, Purchase
from .forms import AddToCartForm
from modules.account.models import Account
from utils import flash_errors, send_email
from datetime import datetime
from database import database
from decorators import login_required


cart = Blueprint(
    "cart", __name__, template_folder="templates", url_prefix="/bookstore/cart")


@cart.route("/", methods=["GET", "POST"])
@login_required
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
    except Book.DoesNotExist:
        flash("We don't have any books with that ISBN :/", "error")
        return redirect(url_for('.show_cart'))
    current_cart = session.get("cart", [])
    if current_cart.count(b.serialize()) >= b.count:
        flash("Unable to add - not in stock", "error")
        return redirect(url_for(".show_cart"))
    current_cart.append(b.serialize())
    session["cart"] = current_cart
    current_total = session.get("total", 0)
    current_total += b.price
    session["total"] = current_total
    flash("Added {} to cart".format(b.title), "success")
    return redirect(url_for('.show_cart'))


@cart.route("/remove/", methods=["POST"])
@login_required
def remove_item():
    current_cart = session.get("cart", [])
    b = Book.get(Book.isbn == request.form.get("remove_isbn"))
    current_cart.remove(b.serialize())
    session["cart"] = current_cart
    current_total = session.get("total", 0)
    current_total -= b.price
    session["total"] = current_total
    return redirect(url_for('.show_cart'))


@cart.route("/clear/")
@login_required
def clear_cart():
    session["cart"] = []
    session["total"] = 0
    return redirect(url_for('.show_cart'))


@cart.route("/purchase/", methods=["POST"])
@login_required
def complete_purchase():
    method = request.form.get("saleType", "sale")
    comment = request.form.get("saleComment", "No Comment")
    cart = session.get("cart", [])
    if len(cart) < 1:
        flash("No Books in Cart", "error")
        return redirect(url_for(".show_cart"))
    books_to_email = []
    for book in cart:
        p = Purchase.create(
            time=datetime.now(), seller=g.user, method=method, comment=comment)
        b = Book.get(Book.isbn == book.get("isbn"))
        if method == "return":
            return_book_transaction(p, b)
        else:
            add_book_to_purchase(p, b)
        if b.count < 5:
            books_to_email.append(b)
    if current_app.config["SEND_INVENTORY_ALERTS"]:
        if len(books_to_email) > 0:
            accounts = Account.select().where(Account.admin == True)
            recipients = []
            for account in accounts:
                if not account.disabled:
                    recipients.append(account.email)
        for b in list(set(books_to_email)):
            send_email(current_app.config["MAIL_FROM"],
                       recipients,
                       "Low Inventory Alert ({}) - {}".format(
                           current_app.config["ENVIRONMENT"], b.title),
                       render_template('cart/low_inventory.txt', book=b),
                       render_template('cart/low_inventory.html', book=b))
    flash("Completed Purchase and Updated Inventory", "success")
    return redirect(url_for('.clear_cart'))


@database.transaction()
def add_book_to_purchase(purchase, book):
    purchase.books.add(book)
    purchase.total = book.price
    book.count -= 1
    purchase.save()
    book.save()


@database.transaction()
def return_book_transaction(purchase, book):
    purchase.books.add(book)
    purchase.total = book.price * -1
    book.count += 1
    purchase.save()
    book.save()
