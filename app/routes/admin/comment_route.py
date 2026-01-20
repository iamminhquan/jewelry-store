from flask import Blueprint, render_template

from app.decorators import admin_required


comment_bp = Blueprint(
    "comment",
    __name__,
    url_prefix="/admin/danhgia",
)


@comment_bp.route("/", methods=["GET"])
@admin_required
def show_comment_page():
    """Hiển thị trang quản lý đánh giá."""
    return render_template("admin/comment/comment.html")
