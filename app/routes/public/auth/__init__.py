from flask import Blueprint

bp: Blueprint = Blueprint("auth", __name__, url_prefix="/auth")

from . import routes as auth_routes
