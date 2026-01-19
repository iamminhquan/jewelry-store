from flask import Blueprint, render_template


admin_route = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_route.route("/", methods=["GET"])
def show_dashboard_page():
    """Hiển thị trang tổng quan quản trị.

    Returns:
        Response: Template trang tổng quan quản trị đã render.
    """
    return render_template("admin/index.html")
