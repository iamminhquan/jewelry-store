"""
Module route đơn hàng người dùng.

Blueprint này xử lý các thao tác đơn hàng phía người dùng bao gồm:
- Xem danh sách đơn hàng
- Tạo đơn hàng từ giỏ hàng
- Xem chi tiết đơn hàng
- Hủy đơn hàng
- Lịch sử mua hàng
- Xem hóa đơn
"""

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.constants import OrderStatus
from app.services.invoice_detail_service import get_invoice_detail_with_product
from app.services.invoice_service import get_invoices_by_user
from app.services.user_order_service import (
    build_purchase_history,
    cancel_user_order,
    create_order_from_cart,
    get_active_cart,
    get_cart_details,
    get_related_order,
    get_user_completed_orders,
    get_user_invoice_or_none,
    get_user_order_or_none,
    get_user_orders,
)

user_order_bp = Blueprint(
    "user_order",
    __name__,
    url_prefix="/order",
)


# -----------------------------------------------------------------------------
# Danh sách & Chi tiết đơn hàng
# -----------------------------------------------------------------------------

@user_order_bp.route("/", methods=["GET"])
@login_required
def show_orders():
    """Hiển thị tất cả đơn hàng của người dùng hiện tại.

    Returns:
        Template được render với danh sách đơn hàng của người dùng.
    """
    orders = get_user_orders(current_user.ma_tai_khoan)

    return render_template(
        "user/orders.html",
        orders=orders,
        OrderStatus=OrderStatus
    )


@user_order_bp.route("/<int:order_id>")
@login_required
def show_order_detail(order_id: int):
    """Hiển thị chi tiết đơn hàng của người dùng hiện tại.

    Args:
        order_id: Mã đơn hàng cần hiển thị.

    Returns:
        Template được render với chi tiết đơn hàng.
    """
    order = get_user_order_or_none(order_id, current_user.ma_tai_khoan)
    if order is None:
        abort(404)

    return render_template(
        "user/order.html",
        order=order,
        OrderStatus=OrderStatus
    )


# -----------------------------------------------------------------------------
# Tạo đơn hàng
# -----------------------------------------------------------------------------

@user_order_bp.route("/", methods=["POST"])
@login_required
def create_order():
    """Tạo đơn hàng mới từ giỏ hàng đang hoạt động của người dùng.

    Dữ liệu form mong đợi:
        - full_name: Họ tên khách hàng (bắt buộc)
        - phone: Số điện thoại khách hàng (bắt buộc)
        - address: Địa chỉ giao hàng (bắt buộc)
        - payment_method: Phương thức thanh toán (tùy chọn)

    Returns:
        Chuyển hướng đến trang chi tiết đơn hàng khi thành công.
        Trả về lỗi 400 nếu validate thất bại.
    """
    # Validate các trường bắt buộc
    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    address = request.form.get("address")

    if not all([full_name, phone, address]):
        abort(400)

    # Lấy giỏ hàng đang hoạt động
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        abort(404)

    # Lấy các sản phẩm trong giỏ hàng
    cart_details = get_cart_details(cart.ma_gio_hang)
    if not cart_details:
        abort(400)

    # Tạo đơn hàng từ giỏ hàng
    order = create_order_from_cart(
        user_id=current_user.ma_tai_khoan,
        cart=cart,
        cart_details=cart_details
    )

    return redirect(url_for("user_order.show_order_detail", order_id=order.ma_don_hang))


# -----------------------------------------------------------------------------
# Hủy đơn hàng
# -----------------------------------------------------------------------------

@user_order_bp.route("/<int:order_id>/cancel", methods=["POST"])
@login_required
def cancel_order(order_id: int):
    """Hủy đơn hàng (do người dùng thực hiện).

    Người dùng chỉ có thể hủy đơn hàng của mình khi đang ở trạng thái
    Chờ xử lý hoặc Đang xử lý.

    Args:
        order_id: Mã đơn hàng cần hủy.

    Returns:
        Chuyển hướng đến trang danh sách đơn hàng kèm thông báo flash.
    """
    order = get_user_order_or_none(order_id, current_user.ma_tai_khoan)
    if order is None:
        abort(404)

    success = cancel_user_order(order)

    if success:
        flash("Đơn hàng đã được hủy thành công.", "success")
    else:
        flash("Không thể hủy đơn hàng này. Đơn hàng đang được giao hoặc đã hoàn thành.", "error")

    return redirect(url_for("user_order.show_orders"))


# -----------------------------------------------------------------------------
# Lịch sử mua hàng
# -----------------------------------------------------------------------------

@user_order_bp.route("/purchase-history")
@login_required
def show_purchase_history():
    """Hiển thị lịch sử mua hàng (đơn hàng đã hoàn thành kèm hóa đơn) của người dùng.

    Returns:
        Template được render với lịch sử mua hàng của người dùng.
    """
    user_id = current_user.ma_tai_khoan

    completed_orders = get_user_completed_orders(user_id)
    invoices = get_invoices_by_user(user_id)
    purchase_history = build_purchase_history(completed_orders, invoices)

    return render_template(
        "user/purchase_history.html",
        purchase_history=purchase_history,
        OrderStatus=OrderStatus
    )


# -----------------------------------------------------------------------------
# Chi tiết hóa đơn
# -----------------------------------------------------------------------------

@user_order_bp.route("/invoice/<int:invoice_id>")
@login_required
def show_invoice_detail(invoice_id: int):
    """Hiển thị chi tiết hóa đơn của người dùng hiện tại.

    Args:
        invoice_id: Mã hóa đơn cần hiển thị.

    Returns:
        Template được render với chi tiết hóa đơn.
    """
    invoice = get_user_invoice_or_none(invoice_id, current_user.ma_tai_khoan)
    if invoice is None:
        abort(404)

    invoice_details = get_invoice_detail_with_product(invoice_id)
    order = get_related_order(invoice)

    return render_template(
        "user/invoice_detail.html",
        invoice=invoice,
        order=order,
        invoice_details=invoice_details,
        OrderStatus=OrderStatus
    )
