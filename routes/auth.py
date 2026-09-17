from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models import User, db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("students.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("students.dashboard"))
        flash("Invalid username or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("students.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or len(username) < 3:
            flash("Username must contain at least 3 characters.", "danger")
        elif len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
        elif password != confirm:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. You can now log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
