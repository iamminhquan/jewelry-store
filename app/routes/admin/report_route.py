from flask import Blueprint, render_template

from app.services.report_service import build_report_data


report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/admin/report",
)


@report_bp.route("/", methods=["GET"])
def show_report_page():
    """Hiển thị trang báo cáo doanh thu và lượt mua."""
    report_data = build_report_data()
    return render_template("admin/report/report.html", **report_data)
