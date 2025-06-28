from flask import Blueprint, render_template, request, redirect, flash, url_for
from models.user import User
from extensions import db
from flask_login import login_user, logout_user, login_required
from extensions import login_manager

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def home():
    return redirect("/dashboard")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "login_success")
            return redirect("/dashboard")
        else:
            flash("Invalid credentials", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registered successfully", "success")
            return redirect("/login")
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect("/login")
