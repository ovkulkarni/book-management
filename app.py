from database import database
from flask import Flask, render_template, flash, redirect, make_response, request, session
from flask_wtf.csrf import CsrfProtect
import logging
import subprocess
import traceback
import os


log_formatter = logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s
Message:
%(message)s
''')

csrf = CsrfProtect()

def create_app(environment):
    app = Flask(__name__)
    app.config.from_pyfile("config/{}.py".format(environment))

    database.init(app.config["DB_PATH"])

    from modules.inventory.blueprint import inventory
    from modules.cart.blueprint import cart

    app.register_blueprint(cart)
    app.register_blueprint(inventory)

    csrf.init_app(app)
    
    @app.route("/favicon.ico")
    def favicon(): return redirect('/static/favicon.ico')

    @app.route("/robots.txt")
    def robots_txt(): return redirect('/static/robots.txt')

    @app.context_processor
    def inject_config():
        if app.config["DISPLAY_DEBUG_INFO"]:
            version = subprocess.check_output(["git", "describe", "--always"]).decode().strip()
        else:
            version = ""
        return dict(global_config=app.config, version=version)

    @app.errorhandler(404)
    def page_not_found(exc):
        return make_response(render_template("not_found.html"), 404)

    @app.errorhandler(500)
    def internal_error(exc):
        trace = traceback.format_exc()
        return make_response(render_template("internal_error.html", trace=trace), 500)

    @csrf.error_handler
    def csrf_error(reason):
        return make_response(render_template('csrf_error.html', reason=reason), 400)

    @app.route("/")
    def home_page():
        return render_template("base.html")

    @csrf.exempt
    @app.route("/github/<key>/", methods=["POST"])
    def git_hook(key):
        if not app.config["ENVIRONMENT"] == "staging":
            return make_response("Github Hook is disabled", 200)
        if key != os.getenv("GITHUB_KEY", ""):
            return make_response(render_template('csrf_error.html'), 400)
        out = subprocess.check_output(["git", "pull"]).decode().strip()
        return make_response(str(out), 200)

    return app

if __name__ == '__main__':
    create_app("dev").run(port=5000, debug=True)
