from flask import Blueprint, render_template
from flask import send_file
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime

from app.decorators import admin_required
from app.services.report_service import build_report_data



report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/admin/report",
)


@report_bp.route("/", methods=["GET"])
@admin_required
def show_report_page():
    """Hiển thị trang báo cáo doanh thu và lượt mua."""
    report_data = build_report_data()
    return render_template("admin/report/report.html", **report_data)


@report_bp.route("/export-excel", methods=["GET"])
@admin_required
def export_report_excel():
    """Xuất báo cáo doanh thu và lượt mua dưới dạng file Excel."""
    report_data = build_report_data()

    revenue = report_data["revenue_stats"]
    purchase = report_data["purchase_stats"]
    status_list = report_data["status_breakdown"]

    # page1
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Tổng quan"

    ws1.append(["Thông tin", "Giá trị"])
    ws1.append(["Tổng doanh thu", revenue["total_revenue"]])
    ws1.append(["Tổng lượt mua", purchase["total_orders"]])
    ws1.append(["Giá trị đơn trung bình", purchase["avg_order_value"]])
    ws1.append(["Tỷ lệ huỷ đơn (%)", purchase["cancel_rate"]])

    for cell in ws1[1]:
        cell.font = Font(bold=True)
    ws1.freeze_panes = "A2"

    # page2
    ws2 = wb.create_sheet(title="Trạng thái đơn hàng")
    ws2.append(["Trạng thái", "Số đơn", "Tỷ lệ (%)"])
    for item in status_list:
        ws2.append([item["label"], item["value"], item["percent"]])
    for cell in ws2[1]:
        cell.font = Font(bold=True)

    ws2.freeze_panes = "A2"

    # export
    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    filename = f"bao_cao_doanhthu{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    return send_file(
        file_stream,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
