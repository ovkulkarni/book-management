import xlsxwriter

def generate_purchase_spreadsheet(purchases):
	workbook = xlsxwriter.Workbook('report.xlsx')
	worksheet = workbook.add_worksheet("Report")
	bold = workbook.add_format({'bold': True})
	money = workbook.add_format({'num_format': '$##'})
	worksheet.write(0, 0, "Purchase Time", bold)
	worksheet.write(0, 1, "Book Title", bold)
	worksheet.write(0, 2, "Book ISBN", bold)
	worksheet.write(0, 3, "Purchase Total", bold)
	worksheet.write(0, 4, "Sold By", bold)
	worksheet.write(0, 5, "Type Of Sale", bold)
	row = 1
	for purchase in purchases:
		worksheet.write(row, 0, purchase.time.ctime())
		worksheet.write(row, 1, purchase.book.title)
		worksheet.write(row, 2, purchase.book.isbn)
		worksheet.write(row, 3, purchase.total, money)
		worksheet.write(row, 4, purchase.seller.name)
		worksheet.write(row, 5, purchase.method.title())
		row += 1
	worksheet.write(row + 1, 0, "Total Revenue", bold)
	worksheet.write(row + 1, 1, "=SUM(D1:D{})".format(row), money)
	worksheet.set_column(0, 5, 20)
	workbook.close()
	return "report.xlsx"

def generate_inventory_spreadsheet(books):
	workbook = xlsxwriter.Workbook('inventory.xlsx')
	worksheet = workbook.add_worksheet("Report")
	bold = workbook.add_format({'bold': True})
	money = workbook.add_format({'num_format': '$##'})
	worksheet.write(0, 0, "Book Title", bold)
	worksheet.write(0, 1, "Book ISBN", bold)
	worksheet.write(0, 2, "Book Price", bold)
	worksheet.write(0, 3, "Book Quantity", bold)
	worksheet.write(0, 4, "Amount", bold)
	row = 1
	for book in books:
		worksheet.write(row, 0, book.title)
		worksheet.write(row, 1, book.isbn)
		worksheet.write(row, 2, book.price, money)
		worksheet.write(row, 3, book.count)
		worksheet.write(row, 4, "=PRODUCT(C{}:D{})".format(row+1, row+1))
		row += 1
	worksheet.set_column(0, 4, 20)
	workbook.close()
	return "inventory.xlsx"

def generate_receipt_spreadsheet(receipts):
	workbook = xlsxwriter.Workbook('receipt.xlsx')
	worksheet = workbook.add_worksheet("Report")
	bold = workbook.add_format({'bold': True})
	money = workbook.add_format({'num_format': '$##'})
	worksheet.write(0, 0, "Book Name", bold)
	worksheet.write(0, 1, "Quantity Added", bold)
	worksheet.write(0, 2, "Unit Price", bold)
	worksheet.write(0, 3, "Invoice Number", bold)
	worksheet.write(0, 4, "Invoice Date", bold)
	worksheet.write(0, 5, "Added By", bold)
	worksheet.write(0, 6, "Added At", bold)
	row = 1
	for receipt in receipts:
		worksheet.write(row, 0, receipt.book.title)
		worksheet.write(row, 1, receipt.quantity)
		worksheet.write(row, 2, receipt.unit_price, money)
		worksheet.write(row, 3, receipt.invoice_number)
		worksheet.write(row, 4, receipt.invoice_date.strftime("%Y-%m-%d"))
		worksheet.write(row, 5, receipt.user.name)
		worksheet.write(row, 6, receipt.date.ctime())
		row += 1
	worksheet.set_column(0, 6, 20)
	workbook.close()
	return "receipt.xlsx"