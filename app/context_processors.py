"""
Context processors for Flask templates.
"""
from flask import g
from flask_login import current_user


def app_context_Processor():
    """Add global variables to all templates."""
    SITE_INFO = {
        "site_title": "Armstrong Number Calculator",
        "site_tagline": "Discover and explore Armstrong numbers"
    }
    
    # Get current user profile if logged in
    CURRENT_USER = None
    if current_user.is_authenticated:
        CURRENT_USER = current_user.profile if hasattr(current_user, 'profile') and current_user.profile else None
    
    return {
        "SITE_INFO": SITE_INFO,
        "CURRENT_USER": CURRENT_USER,
        "current_user": current_user
    }
