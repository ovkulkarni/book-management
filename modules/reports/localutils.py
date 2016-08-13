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
	row = 1
	for purchase in purchases:
		worksheet.write(row, 0, purchase.time.ctime())
		worksheet.write(row, 1, purchase.book.title)
		worksheet.write(row, 2, purchase.book.isbn)
		worksheet.write(row, 3, purchase.total, money)
		worksheet.write(row, 4, purchase.seller.name)
		row += 1
	worksheet.write(row + 1, 0, "Total Revenue", bold)
	worksheet.write(row + 1, 1, "=SUM(D1:D{})".format(row), money)
	worksheet.set_column(0, 4, 20)
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
	worksheet.set_column(0, 3, 20)
	workbook.close()
	return "inventory.xlsx"