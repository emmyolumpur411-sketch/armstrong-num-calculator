"""
Contact and feedback routes.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models.feedback import Feedback

from . import bp


@bp.route("/", methods=["GET"])
def index():
    """Contact us page."""
    return render_template("public/pages/contact/index.html")


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    """Submit feedback form."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        
        # Validation
        if not name or len(name) < 2:
            flash("Name must be at least 2 characters long.", "error")
            return render_template("public/pages/contact/feedback.html",
                                 name=name, email=email, subject=subject, message=message)
        
        if not email or "@" not in email:
            flash("Please enter a valid email address.", "error")
            return render_template("public/pages/contact/feedback.html",
                                 name=name, email=email, subject=subject, message=message)
        
        if not message or len(message) < 10:
            flash("Message must be at least 10 characters long.", "error")
            return render_template("public/pages/contact/feedback.html",
                                 name=name, email=email, subject=subject, message=message)
        
        try:
            # Create feedback
            feedback = Feedback()
            feedback.name = name
            feedback.email = email
            feedback.subject = subject
            feedback.message = message
            
            # Link to user if logged in
            if current_user.is_authenticated:
                feedback.user_id = current_user.id
            
            feedback.save()
            
            flash("Thank you for your feedback! We'll get back to you soon.", "success")
            return redirect(url_for("web.web_public.contact.feedback"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Error submitting feedback: {str(e)}", "error")
            return render_template("public/pages/contact/feedback.html",
                                 name=name, email=email, subject=subject, message=message)
    
    return render_template("public/pages/contact/feedback.html")
