"""
User order routes module.

This blueprint handles user-facing order operations including:
- Viewing orders list
- Creating orders from cart
- Viewing order details
- Cancelling orders
- Purchase history
- Invoice viewing
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
# Order List & Detail Routes
# -----------------------------------------------------------------------------

@user_order_bp.route("/", methods=["GET"])
@login_required
def show_orders():
    """Display all orders for the current user.

    Returns:
        Rendered template with user's orders list.
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
    """Display order detail for the current user.

    Args:
        order_id: The order ID to display.

    Returns:
        Rendered template with order details.
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
# Order Creation
# -----------------------------------------------------------------------------

@user_order_bp.route("/", methods=["POST"])
@login_required
def create_order():
    """Create a new order from the user's active cart.

    Expected form data:
        - full_name: Customer full name (required)
        - phone: Customer phone number (required)
        - address: Delivery address (required)
        - payment_method: Payment method (optional)

    Returns:
        Redirect to order detail page on success.
        Aborts with 400 if validation fails.
    """
    # Validate required fields
    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    address = request.form.get("address")

    if not all([full_name, phone, address]):
        abort(400)

    # Get active cart
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        abort(404)

    # Get cart items
    cart_details = get_cart_details(cart.ma_gio_hang)
    if not cart_details:
        abort(400)

    # Create order from cart
    order = create_order_from_cart(
        user_id=current_user.ma_tai_khoan,
        cart=cart,
        cart_details=cart_details
    )

    return redirect(url_for("user_order.show_order_detail", order_id=order.ma_don_hang))


# -----------------------------------------------------------------------------
# Order Cancellation
# -----------------------------------------------------------------------------

@user_order_bp.route("/<int:order_id>/cancel", methods=["POST"])
@login_required
def cancel_order(order_id: int):
    """Cancel an order (user-initiated).

    Users can only cancel their own orders that are in Pending or Processing status.

    Args:
        order_id: The order ID to cancel.

    Returns:
        Redirect to orders page with flash message.
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
# Purchase History
# -----------------------------------------------------------------------------

@user_order_bp.route("/purchase-history")
@login_required
def show_purchase_history():
    """Display purchase history (completed orders with invoices) for the current user.

    Returns:
        Rendered template with user's purchase history.
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
# Invoice Detail
# -----------------------------------------------------------------------------

@user_order_bp.route("/invoice/<int:invoice_id>")
@login_required
def show_invoice_detail(invoice_id: int):
    """Display invoice detail for the current user.

    Args:
        invoice_id: The invoice ID to display.

    Returns:
        Rendered template with invoice details.
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
