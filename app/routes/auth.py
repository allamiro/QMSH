from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        if request.form.get("password"):
            current_user.password_hash = generate_password_hash(request.form.get("password"))
        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html", user=current_user)
