from flask import Blueprint, redirect, render_template, session, url_for, request
from flask_login import current_user, login_required, logout_user
from app.extensions import db


main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/",
)


@main_bp.route("/")
def show_home_page():
    return render_template("index.html")


@main_bp.route("/about")
def show_about_page():
    return render_template("about.html")


@main_bp.route("/login")
def show_login_page():
    return redirect(url_for("auth.show_sign_in_page"))


@main_bp.route("/register")
def show_register_page():
    return redirect(url_for("auth.show_sign_up_page"))


@main_bp.route("/account", methods=["GET", "POST"])
@login_required
def show_account_page():
    if request.method == "POST":
        user = current_user
        user.ho_ten = request.form.get("ho_ten")
        user.email = request.form.get("email")
        user.so_dien_thoai = request.form.get("so_dien_thoai")
        user.dia_chi = request.form.get("dia_chi")
        user.gioi_tinh = request.form.get("gioi_tinh")
        user.ngay_sinh = request.form.get("ngay_sinh") or None

        db.session.commit()

    return render_template(
        "account.html",
        user=current_user,
    )


@main_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("main.show_home_page"))
