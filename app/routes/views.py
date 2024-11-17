from flask import Blueprint, redirect, url_for
from flask_login import current_user

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return redirect(url_for("compliance.dashboard"))  # Redirect authenticated users to the dashboard
