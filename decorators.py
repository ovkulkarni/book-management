from flask import session, request, g, flash, redirect, url_for
from functools import wraps

def login_required(f):
	@wraps(f)
	def _decorated(*args, **kwargs):
		if g.user is not None:
			return f(*args, **kwargs)
		else:
			flash("You must be logged in to perform this action.", "alert")
			return redirect(url_for("account.login", next=request.path))
	return _decorated

def admin_required(f):
	@wraps(f)
	def _decorated(*args, **kwargs):
		if g.user is not None:
			if g.user.admin:
				return f(*args, **kwargs)
			else:
				flash("You must be an admin to perform this action.", "alert")
				return redirect(url_for('home_page'))
		else:
			flash("You must be logged in to perform this action.", "alert")
			return redirect(url_for("account.login", next=request.path))
	return _decorated