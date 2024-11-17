from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        flash("Logged in successfully!", "success")
        return redirect(url_for("views.home"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("auth.login"))


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
