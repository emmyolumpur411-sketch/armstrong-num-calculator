"""
Authentication routes for public users.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import re

from app.extensions import db
from app.models.user import AppUser, Profile, Address
from app.models.wallet import Wallet
from app.utils.helpers.validate import validate_json_data

from . import bp


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Basic phone validation - digits only, 10-15 digits
    pattern = r'^\d{10,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None


@bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration page."""
    if request.method == "POST":
        # Get form data
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        # Validation
        errors = []
        
        if not name or len(name) < 2:
            errors.append("Name must be at least 2 characters long.")
        
        if not validate_email(email):
            errors.append("Please enter a valid email address.")
        
        if not validate_phone(phone):
            errors.append("Please enter a valid phone number (10-15 digits).")
        
        if not username or len(username) < 3:
            errors.append("Username must be at least 3 characters long.")
        
        if not password or len(password) < 6:
            errors.append("Password must be at least 6 characters long.")
        
        if password != confirm_password:
            errors.append("Passwords do not match.")
        
        # Check if email or username already exists
        if AppUser.query.filter_by(email=email).first():
            errors.append("Email already registered.")
        
        if AppUser.query.filter_by(username=username).first():
            errors.append("Username already taken.")
        
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("public/pages/auth/register.html", 
                                 name=name, email=email, phone=phone, username=username)
        
        # Create user
        try:
            # Split name into firstname and lastname
            name_parts = name.split(maxsplit=1)
            firstname = name_parts[0] if name_parts else name
            lastname = name_parts[1] if len(name_parts) > 1 else ""
            
            # Create user
            new_user = AppUser()
            new_user.email = email
            new_user.username = username
            new_user.password = password
            
            db.session.add(new_user)
            db.session.flush()  # Get user ID
            
            # Create profile
            profile = Profile()
            profile.user_id = new_user.id
            profile.firstname = firstname
            profile.lastname = lastname
            profile.phone = phone
            
            # Create address
            address = Address()
            address.user_id = new_user.id
            
            # Create wallet
            wallet = Wallet()
            wallet.user_id = new_user.id
            
            db.session.add_all([profile, address, wallet])
            db.session.commit()
            
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("web.web_public.auth.login"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "error")
            return render_template("public/pages/auth/register.html",
                                 name=name, email=email, phone=phone, username=username)
    
    return render_template("public/pages/auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for("web.web_public.home.index"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"
        
        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("public/pages/auth/login.html", username=username)
        
        # Find user by username or email
        user = AppUser.query.filter(
            (AppUser.username == username) | (AppUser.email == username)
        ).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f"Welcome back, {user.profile.firstname if user.profile else user.username}!", "success")
            
            # Redirect to next page or home
            next_page = request.args.get("next")
            return redirect(next_page or url_for("web.web_public.home.index"))
        else:
            flash("Invalid username or password.", "error")
            return render_template("public/pages/auth/login.html", username=username)
    
    return render_template("public/pages/auth/login.html")


@bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """User logout."""
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("web.web_public.home.index"))
