from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from urllib.parse import urlparse

from app.services.auth_service import authenticate_user, register_user

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def show_sign_in_page():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        account, error_message = authenticate_user(identifier, password)
        if not account:
            flash(error_message, "error")
            return redirect(url_for("auth.show_sign_in_page"))

        login_user(account, remember=remember)

        # Check for safe next_url first (e.g., from @login_required redirect)
        next_url = request.args.get("next")
        if next_url and urlparse(next_url).netloc == "":
            return redirect(next_url)

        # Redirect all users to home page after login
        return redirect(url_for("main.show_home_page"))

    return render_template("auth/sign_in.html")


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def show_sign_up_page():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        account, error_message = register_user(
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password,
            full_name=full_name,
            phone=phone,
        )
        if not account:
            flash(error_message, "error")
            return redirect(url_for("auth.show_sign_up_page"))

        flash("Tạo tài khoản thành công. Vui lòng đăng nhập.", "success")
        return redirect(url_for("auth.show_sign_in_page"))

    return render_template("auth/sign_up.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def show_forgot_password_page():
    return render_template("auth/forgot_password.html")
