from flask import Blueprint

#create blueprint
main = Blueprint("main", __name__, template_folder="templates", static_folder="static", static_url_path="/static/main")

from . import routes