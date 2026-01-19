from flask import Blueprint, render_template


admin_route = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_route.route("/")
def show_dashboard_page():
    return render_template("admin/index.html")
