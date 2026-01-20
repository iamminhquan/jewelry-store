from flask import Blueprint, render_template

from app.decorators import admin_required


admin_route = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_route.route("/", methods=["GET"])
@admin_required  # Chỉ admin (role == 1) mới được truy cập
def show_dashboard_page():
    """Hiển thị trang tổng quan quản trị.

    Returns:
        Response: Template trang tổng quan quản trị đã render.
    """
    return render_template("admin/index.html")
