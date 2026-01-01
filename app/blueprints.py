from typing import List
from flask import Flask, Blueprint

def register_blueprints(app: Flask) -> None:
    """Register all application blueprints, including API and docs."""
    # Lazy imports to avoid circulars during app factory
    
    from .error_handlers.web import attach_web_err_handlers
    
    from .routes import create_web_blueprint
    from .routes.public import create_web_public_blueprint
    from .routes.admin import create_web_admin_blueprint
    
    # Create the blueprints
    web_bp = create_web_blueprint()
    web_public_bp = create_web_public_blueprint()
    web_admin_bp = create_web_admin_blueprint()
    
    # Attach JSON error handlers to all API scopes BEFORE registration
    attach_web_err_handlers(web_admin_bp)
    
    
    # Register the web public blueprint
    register_sub_blueprints(web_bp, [web_public_bp, web_admin_bp])
    
    # Register the web blueprint
    app.register_blueprint(web_bp)


def register_sub_blueprints(bp: Blueprint, blueprints: List[Blueprint]):
    for sub_bp in blueprints:
        bp.register_blueprint(sub_bp)