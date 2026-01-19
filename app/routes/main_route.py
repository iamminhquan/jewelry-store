from flask import Blueprint, render_template


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
