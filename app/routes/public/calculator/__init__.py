from flask import Blueprint

bp: Blueprint = Blueprint("calculator", __name__, url_prefix="/calculator")

from . import routes as calculator_routes
