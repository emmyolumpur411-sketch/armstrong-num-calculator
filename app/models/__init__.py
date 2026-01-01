"""
This package contains the database models for the Flask application.

Each model corresponds to a table in the database.

Author: Emmanuel Olowu
Link: https://github.com/zeddyemy
Copyright: © 2024 Emmanuel Olowu <zeddyemy@gmail.com>
"""
from flask import Flask
from sqlalchemy.orm import aliased

from .user import AppUser, Profile, Address, TempUser
from .role import Role, UserRole
from .attempt import Attempt
from .feedback import Feedback
from .media import Media