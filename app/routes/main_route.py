from flask import Blueprint, render_template
from flask_login import current_user, login_required


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


@main_bp.route("/account")
@login_required
def show_account_page():
    return render_template("account.html", user=current_user)
