"""
Settings routes for user profile and account management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.user import AppUser, Profile, Address

from . import bp


@bp.route("/", methods=["GET"])
@login_required
def index():
    """Settings main page."""
    return render_template("public/pages/settings/index.html")


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Create or update user profile."""
    if request.method == "POST":
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        phone = request.form.get("phone", "").strip()
        gender = request.form.get("gender", "").strip()
        
        # Validation
        if not firstname or len(firstname) < 2:
            flash("First name must be at least 2 characters long.", "error")
            return redirect(url_for("web.web_public.settings.profile"))
        
        try:
            # Get or create profile
            profile = current_user.profile
            if not profile:
                profile = Profile()
                profile.user_id = current_user.id
            
            profile.firstname = firstname
            profile.lastname = lastname
            profile.phone = phone
            profile.gender = gender
            
            db.session.add(profile)
            db.session.commit()
            
            flash("Profile updated successfully!", "success")
            return redirect(url_for("web.web_public.settings.profile"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "error")
            return redirect(url_for("web.web_public.settings.profile"))
    
    return render_template("public/pages/settings/profile.html")


@bp.route("/address", methods=["GET", "POST"])
@login_required
def address():
    """Create or update user address."""
    if request.method == "POST":
        country = request.form.get("country", "").strip()
        state = request.form.get("state", "").strip()
        
        try:
            # Get or create address
            address = current_user.address
            if not address:
                address = Address()
                address.user_id = current_user.id
            
            address.country = country
            address.state = state
            
            db.session.add(address)
            db.session.commit()
            
            flash("Address updated successfully!", "success")
            return redirect(url_for("web.web_public.settings.address"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating address: {str(e)}", "error")
            return redirect(url_for("web.web_public.settings.address"))
    
    return render_template("public/pages/settings/address.html")


@bp.route("/delete-profile", methods=["POST"])
@login_required
def delete_profile():
    """Delete user profile (soft delete by clearing data)."""
    try:
        if current_user.profile:
            current_user.profile.firstname = ""
            current_user.profile.lastname = ""
            current_user.profile.phone = ""
            current_user.profile.gender = ""
            db.session.commit()
            flash("Profile data cleared successfully.", "success")
        else:
            flash("No profile to delete.", "info")
        
        return redirect(url_for("web.web_public.settings.profile"))
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting profile: {str(e)}", "error")
        return redirect(url_for("web.web_public.settings.profile"))
