from __future__ import annotations

from flask import Blueprint


def create_web_admin_blueprint():
    """Create and return the web public blueprint."""
    web_admin_bp = Blueprint("web_admin", __name__, url_prefix="")
    
    return web_admin_bp