from __future__ import annotations

from flask import Blueprint


from .home import bp as home_bp
from .auth import bp as auth_bp
from .calculator import bp as calculator_bp
from .settings import bp as settings_bp
from .contact import bp as contact_bp

def create_web_public_blueprint():
    """Create and return the web public blueprint."""
    web_public_bp = Blueprint("web_public", __name__, url_prefix="")
    
    web_public_bp.register_blueprint(home_bp)
    web_public_bp.register_blueprint(auth_bp)
    web_public_bp.register_blueprint(calculator_bp)
    web_public_bp.register_blueprint(settings_bp)
    web_public_bp.register_blueprint(contact_bp)
    
    return web_public_bp