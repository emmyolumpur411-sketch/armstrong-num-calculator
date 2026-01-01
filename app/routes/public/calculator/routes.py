"""
Armstrong number calculator routes.
"""
import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.attempt import Attempt
from app.utils.armstrong import is_armstrong_number, find_armstrong_numbers_in_range, check_armstrong_with_details

from . import bp


@bp.route("/", methods=["GET"])
@login_required
def index():
    """Calculator main page."""
    return render_template("public/pages/calculator/index.html")


@bp.route("/check", methods=["POST"])
@login_required
def check_number():
    """Check if a single number is an Armstrong number."""
    try:
        number_str = request.form.get("number", "").strip()
        
        if not number_str:
            flash("Please enter a number.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        try:
            number = int(number_str)
        except ValueError:
            flash("Please enter a valid integer.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        if number < 0:
            flash("Please enter a non-negative number.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        # Check if Armstrong number
        is_armstrong, details = check_armstrong_with_details(number)
        
        # Save attempt
        attempt = Attempt()
        attempt.user_id = current_user.id
        attempt.input_value = str(number)
        attempt.input_type = "single"
        attempt.is_armstrong = is_armstrong
        attempt.result = json.dumps(details)
        attempt.save()
        
        # Flash result
        if is_armstrong:
            flash(f"{number} is an Armstrong number! {details['calculation']}", "success")
        else:
            flash(f"{number} is NOT an Armstrong number. {details['calculation']}", "info")
        
        return render_template("public/pages/calculator/index.html", 
                             check_result=details, 
                             checked_number=number)
    
    except Exception as e:
        flash(f"Error checking number: {str(e)}", "error")
        return redirect(url_for("web.web_public.calculator.index"))


@bp.route("/range", methods=["POST"])
@login_required
def find_range():
    """Find all Armstrong numbers in a range."""
    try:
        min_str = request.form.get("min_number", "").strip()
        max_str = request.form.get("max_number", "").strip()
        
        if not min_str or not max_str:
            flash("Please enter both minimum and maximum numbers.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        try:
            min_num = int(min_str)
            max_num = int(max_str)
        except ValueError:
            flash("Please enter valid integers.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        if min_num < 0:
            flash("Minimum number must be non-negative.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        if max_num < min_num:
            flash("Maximum number must be greater than or equal to minimum number.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        # Limit range to prevent performance issues
        if max_num - min_num > 1000000:
            flash("Range too large. Please use a range of 1,000,000 or less.", "error")
            return redirect(url_for("web.web_public.calculator.index"))
        
        # Find Armstrong numbers
        armstrong_numbers = find_armstrong_numbers_in_range(min_num, max_num)
        
        # Save attempt
        attempt = Attempt()
        attempt.user_id = current_user.id
        attempt.input_value = f"{min_num}-{max_num}"
        attempt.input_type = "range"
        attempt.count = len(armstrong_numbers)
        attempt.result = json.dumps({"numbers": armstrong_numbers})
        attempt.save()
        
        # Flash result
        if armstrong_numbers:
            flash(f"Found {len(armstrong_numbers)} Armstrong number(s) in range {min_num}-{max_num}.", "success")
        else:
            flash(f"No Armstrong numbers found in range {min_num}-{max_num}.", "info")
        
        return render_template("public/pages/calculator/index.html",
                             range_result=armstrong_numbers,
                             min_num=min_num,
                             max_num=max_num)
    
    except Exception as e:
        flash(f"Error finding range: {str(e)}", "error")
        return redirect(url_for("web.web_public.calculator.index"))


@bp.route("/attempts", methods=["GET"])
@login_required
def attempts():
    """View user's attempt history."""
    page = request.args.get("page", 1, type=int)
    per_page = 20
    
    attempts_query = Attempt.query.filter_by(user_id=current_user.id).order_by(Attempt.created_at.desc())
    attempts_paginated = attempts_query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Parse results for display
    attempts_list = []
    for attempt in attempts_paginated.items:
        attempt_dict = attempt.to_dict()
        try:
            attempt_dict["result_data"] = json.loads(attempt.result) if attempt.result else None
        except:
            attempt_dict["result_data"] = attempt.result
        attempts_list.append(attempt_dict)
    
    return render_template("public/pages/calculator/attempts.html",
                         attempts=attempts_list,
                         pagination=attempts_paginated)
