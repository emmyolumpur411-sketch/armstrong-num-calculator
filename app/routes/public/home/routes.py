from __future__ import annotations

from flask import Blueprint, redirect, url_for, render_template

from . import bp

@bp.route("/", methods=["GET"])
def index():
    return render_template("public/pages/home/index.html")