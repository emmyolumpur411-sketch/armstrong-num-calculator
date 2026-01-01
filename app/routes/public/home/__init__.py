from flask import Blueprint

bp: Blueprint = Blueprint("home", __name__, url_prefix="")

from . import routes as home_routes