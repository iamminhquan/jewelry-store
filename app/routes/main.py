from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Trang chủ"""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Trang giới thiệu"""
    return render_template("about.html")
