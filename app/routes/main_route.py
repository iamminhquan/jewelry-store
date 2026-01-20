from flask import Blueprint, redirect, render_template, session, url_for
from flask_login import current_user, login_required, logout_user


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


@main_bp.route("/account")
@login_required
def show_account_page():
    return render_template("account.html", user=current_user)


@main_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("main.show_home_page"))
