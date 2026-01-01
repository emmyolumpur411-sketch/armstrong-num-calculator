from flask import Blueprint

bp: Blueprint = Blueprint("contact", __name__, url_prefix="/contact")

from . import routes as contact_routes
