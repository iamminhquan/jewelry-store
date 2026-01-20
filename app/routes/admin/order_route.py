from flask import Blueprint, render_template, redirect, request, url_for, flash

from app.services.order_service import (
    cancel_order,
    confirm_order,
    get_order_or_404,
    get_order_page,
    update_order,
    update_order_status,
)
from app.services.order_detail_service import get_order_detail_with_product
from app.models.account import Account


order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/admin/order",
)


@order_bp.route("/", methods=["GET"])
def show_order_page():
    """Hiển thị trang quản lý đơn hàng kèm lọc và phân trang.

    Returns:
        Response: Template danh sách đơn hàng đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()
    min_value = request.args.get("min_value", "").strip()
    max_value = request.args.get("max_value", "").strip()
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        orders,
        total_orders,
        cho_xac_nhan,
        dang_xu_ly,
        dang_giao,
        da_giao,
        da_huy,
    ) = get_order_page(keyword, status, date_from, date_to, min_value, max_value, page)

    # Lấy thông tin khách hàng cho mỗi đơn hàng
    orders_with_account = []
    for order in orders:
        account = Account.query.get(order.ma_tai_khoan)
        orders_with_account.append({
            'order': order,
            'account': account
        })

    return render_template(
        "admin/order/order.html",
        orders_with_account=orders_with_account,
        pagination=pagination,
        total_orders=total_orders,
        cho_xac_nhan=cho_xac_nhan,
        dang_xu_ly=dang_xu_ly,
        dang_giao=dang_giao,
        da_giao=da_giao,
        da_huy=da_huy,
    )


@order_bp.route("/detail/<int:id>", methods=["GET"])
def show_order_detail_page(id):
    """Hiển thị chi tiết đơn hàng.

    Args:
        id (int): Mã đơn hàng.

    Returns:
        Response: Template chi tiết đơn hàng đã render.
    """
    order = get_order_or_404(id)
    account = Account.query.get(order.ma_tai_khoan)
    order_details_with_product = get_order_detail_with_product(id)

    return render_template(
        "admin/order/order_detail.html",
        order=order,
        account=account,
        order_details_with_product=order_details_with_product,
    )


@order_bp.route("/confirm/<int:id>", methods=["POST"])
def confirm_order_route(id):
    """Xác nhận đơn hàng.

    Args:
        id (int): Mã đơn hàng.

    Returns:
        Response: Chuyển hướng về danh sách đơn hàng.
    """
    order = get_order_or_404(id)
    confirm_order(order)
    flash("Đơn hàng đã được xác nhận thành công.", "success")
    return redirect(url_for("order.show_order_page"))


@order_bp.route("/cancel/<int:id>", methods=["POST"])
def cancel_order_route(id):
    """Hủy đơn hàng.

    Args:
        id (int): Mã đơn hàng.

    Returns:
        Response: Chuyển hướng về danh sách đơn hàng.
    """
    order = get_order_or_404(id)
    
    # Kiểm tra điều kiện hủy đơn hàng
    if order.trang_thai in [3, 4]:  # Đã giao hoặc đã hủy
        flash("Không thể hủy đơn hàng này.", "error")
    else:
        cancel_order(order)
        flash("Đơn hàng đã được hủy thành công.", "success")
    
    return redirect(url_for("order.show_order_page"))


@order_bp.route("/update_status/<int:id>", methods=["POST"])
def update_order_status_route(id):
    """Cập nhật trạng thái đơn hàng.

    Args:
        id (int): Mã đơn hàng.

    Returns:
        Response: Chuyển hướng về danh sách đơn hàng.
    """
    order = get_order_or_404(id)
    try:
        new_status = int(request.form.get("trang_thai"))
        update_order_status(order, new_status)
        flash("Trạng thái đơn hàng đã được cập nhật thành công.", "success")
    except (TypeError, ValueError):
        flash("Trạng thái không hợp lệ.", "error")
    
    return redirect(url_for("order.show_order_page"))


@order_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def show_edit_order_page(id):
    """Điều chỉnh thông tin đơn hàng hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã đơn hàng cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    order = get_order_or_404(id)
    account = Account.query.get(order.ma_tai_khoan)

    # Kiểm tra điều kiện chỉnh sửa
    if order.trang_thai in [3, 4]:  # Đã giao hoặc đã hủy
        flash("Không thể chỉnh sửa đơn hàng đã giao hoặc đã hủy.", "error")
        return redirect(url_for("order.show_order_page"))

    if request.method == "POST":
        try:
            tong_tien_tam_tinh = request.form.get("tong_tien_tam_tinh")
            ngay_dat_hang = request.form.get("ngay_dat_hang", "").strip()
            
            tong_tien = float(tong_tien_tam_tinh) if tong_tien_tam_tinh else None
            
            update_order(order, tong_tien, ngay_dat_hang)
            flash("Thông tin đơn hàng đã được cập nhật thành công.", "success")
            return redirect(url_for("order.show_order_page"))
        except (TypeError, ValueError) as e:
            flash("Dữ liệu không hợp lệ.", "error")

    return render_template(
        "admin/order/order_edit.html",
        order=order,
        account=account,
    )
