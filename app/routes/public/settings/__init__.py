from flask import Blueprint

bp: Blueprint = Blueprint("settings", __name__, url_prefix="/settings")

from . import routes as settings_routes
