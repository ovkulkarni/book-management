from flask import Blueprint, render_template, current_app, flash, url_for, request, session, flash, redirect, send_from_directory, g, send_file
from utils import flash_errors
from .localutils import generate_inventory_spreadsheet, generate_purchase_spreadsheet
from modules.cart.models import Purchase, Book
from modules.account.models import Account
from decorators import admin_required
from datetime import date
from dateutil.relativedelta import relativedelta


reports = Blueprint("reports", __name__, template_folder="templates", url_prefix="/reports")

@reports.context_processor
def expose_models():
	return dict(Account=Account, Book=Book)

@reports.route("/")
@admin_required
def index():
	return render_template("reports/index.html")

@reports.route("/generate/inventory/", methods=["POST"])
@admin_required
def generate_inventory_reports():
	if request.form.get("max_quantity", None):
		books = Book.select().where(Book.count <= int(request.form.get("max_quantity"))).order_by(+Book.title)
	else:
		books = Book.select().order_by(+Book.title)
	spreadsheet_path = generate_inventory_spreadsheet(books)
	return send_file(spreadsheet_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", attachment_filename="report.xlsx")

@reports.route("/generate/purchase/", methods=["POST"])
@admin_required
def generate_purchase_reports():
	if not request.form.get("type", None):
		flash("Invalid POST Data", "alert")
		return redirect(url_for('.index'))
	report_type = request.form.get("type")
	if report_type == "user":
		account = Account.get(Account.id == int(request.form.get("user_id")))
		purchases = Purchase.select().where(Purchase.seller == account).order_by(Purchase.time.desc())
	elif report_type == "time":
		one_year_ago = date.today() - relativedelta(years=1)
		one_month_ago = date.today() - relativedelta(months=1)
		one_week_ago = date.today() - relativedelta(weeks=1)
		one_day_ago = date.today()
		length = request.form.get("length")
		if length == "year":
			purchases = Purchase.select().where(Purchase.time > one_year_ago).order_by(Purchase.time.desc())
		elif length == "week":
			purchases = Purchase.select().where(Purchase.time > one_week_ago).order_by(Purchase.time.desc())
		elif length == "month":
			purchases = Purchase.select().where(Purchase.time > one_month_ago).order_by(Purchase.time.desc())
		elif length == "today":
			purchases = Purchase.select().where(Purchase.time > one_day_ago)
		else:
			purchases = Purchase.select().order_by(Purchase.time.desc())
	elif report_type == "book":
		book = Book.get(Book.id == int(request.form.get("book_id")))
		purchases = book.purchases
	elif report_type == "minimum_amount":
		purchases = Purchase.select().where(Purchase.total > int(request.form.get("min_amount")))
	elif report_type == "maximum_amount":
		purchases = Purchase.select().where(Purchase.total < int(request.form.get("max_amount")))
	else:
		purchases = Purchase.select().order_by(Purchase.time.desc())
	spreadsheet_path = generate_purchase_spreadsheet(purchases)
	return send_file(spreadsheet_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", attachment_filename="report.xlsx")



