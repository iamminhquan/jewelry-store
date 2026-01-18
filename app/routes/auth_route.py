from flask import Blueprint, render_template
from app.models.account import Account

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@auth_bp.route("/sign-in")
def show_sign_in_page():
    return render_template("auth/sign_in.html")


@auth_bp.route("/sign-up")
def show_sign_up_page():
    return render_template("auth/sign_up.html")


@auth_bp.route("/forgot-password")
def show_forgot_password_page():
    return render_template("auth/forgot_password.html")
