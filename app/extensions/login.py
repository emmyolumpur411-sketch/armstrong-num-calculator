from flask import Flask
from flask_login import LoginManager, UserMixin, current_user

login_manager: LoginManager = LoginManager()

def init_flask_login(app: Flask):
    login_manager.init_app(app)
    setattr(login_manager, 'login_view', 'web.web_public.auth.login')
    
    @login_manager.user_loader
    def load_user(user_id):
        return load_app_user(user_id, app)
    

def load_app_user(user_id: str, app: Flask):
    """Return the `AppUser` with roles for the given ID, or `None` if missing."""
    from app.models import AppUser
    from app.extensions import db
    from sqlalchemy.orm import joinedload
    from typing import Any, cast
    import uuid

    try:
        user_uuid = uuid.UUID(user_id)
        session = cast(Any, db.session)
        return session.get(AppUser, user_uuid, options=[joinedload(cast(Any, AppUser).roles)])
    except Exception as e:
        app.logger.error(f"Error loading user {user_id}: {e}")
        return None
