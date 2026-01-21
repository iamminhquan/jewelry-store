from flask import Blueprint, render_template

from app.services.dashboard_service import get_dashboard_data, get_website_info


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
    dashboard_data = get_dashboard_data()
    website_info = get_website_info()

    return render_template(
        "admin/index.html",
        **dashboard_data,
        website_info=website_info,
    )
