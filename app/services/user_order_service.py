"""
User order service module.

This module provides business logic for user-facing order operations,
separate from admin order operations in order_service.py.
"""

from typing import Optional

from flask_login import current_user

from app.constants import OrderStatus
from app.extensions import db
from app.models.cart import Cart
from app.models.cart_detail import CartDetail
from app.models.invoice import Invoice
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product


# -----------------------------------------------------------------------------
# Query Helpers
# -----------------------------------------------------------------------------

def get_user_orders(user_id: int) -> list[Order]:
    """Get all orders for a user, sorted by creation date descending.

    Args:
        user_id: The user's account ID.

    Returns:
        List of Order objects belonging to the user.
    """
    return (
        Order.query
        .filter_by(ma_tai_khoan=user_id)
        .order_by(Order.ngay_tao.desc())
        .all()
    )


def get_user_order_or_none(order_id: int, user_id: int) -> Optional[Order]:
    """Get an order that belongs to a specific user.

    Args:
        order_id: The order ID to retrieve.
        user_id: The user's account ID (for ownership verification).

    Returns:
        Order if found and belongs to user, None otherwise.
    """
    return Order.query.filter_by(
        ma_don_hang=order_id,
        ma_tai_khoan=user_id
    ).first()


def get_user_completed_orders(user_id: int) -> list[Order]:
    """Get all completed orders for a user.

    Args:
        user_id: The user's account ID.

    Returns:
        List of completed Order objects, sorted by creation date descending.
    """
    return (
        Order.query
        .filter_by(
            ma_tai_khoan=user_id,
            trang_thai=OrderStatus.COMPLETED
        )
        .order_by(Order.ngay_tao.desc())
        .all()
    )


def get_active_cart(user_id: int) -> Optional[Cart]:
    """Get the active (non-completed) cart for a user.

    Args:
        user_id: The user's account ID.

    Returns:
        Active Cart if found, None otherwise.
    """
    return Cart.query.filter_by(
        ma_tai_khoan=user_id,
        trang_thai=0
    ).first()


def get_cart_details(cart_id: int) -> list[CartDetail]:
    """Get all cart details for a cart.

    Args:
        cart_id: The cart ID.

    Returns:
        List of CartDetail objects.
    """
    return CartDetail.query.filter_by(ma_gio_hang=cart_id).all()


def get_user_invoice_or_none(invoice_id: int, user_id: int) -> Optional[Invoice]:
    """Get an invoice that belongs to a specific user.

    Args:
        invoice_id: The invoice ID to retrieve.
        user_id: The user's account ID (for ownership verification).

    Returns:
        Invoice if found and belongs to user, None otherwise.
    """
    return Invoice.query.filter_by(
        ma_hoa_don=invoice_id,
        ma_tai_khoan=user_id
    ).first()


def get_related_order(invoice: Invoice) -> Optional[Order]:
    """Get the order related to an invoice if it exists.

    Args:
        invoice: The invoice object.

    Returns:
        Order if found and invoice has ma_don_hang, None otherwise.
    """
    if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang:
        return Order.query.get(invoice.ma_don_hang)
    return None


# -----------------------------------------------------------------------------
# Order Creation
# -----------------------------------------------------------------------------

def calculate_cart_total(cart_details: list[CartDetail]) -> float:
    """Calculate the total price from cart details.

    Args:
        cart_details: List of CartDetail objects.

    Returns:
        Total price as float.
    """
    return sum(
        float(detail.so_luong) * float(detail.gia_tai_thoi_diem)
        for detail in cart_details
    )


def create_order_from_cart(user_id: int, cart: Cart, cart_details: list[CartDetail]) -> Order:
    """Create a new order from cart contents.

    This function:
    1. Creates the order with pending status
    2. Creates order details from cart details
    3. Marks the cart as completed (trang_thai=1)

    Args:
        user_id: The user's account ID.
        cart: The cart to convert.
        cart_details: The cart items.

    Returns:
        The newly created Order.
    """
    total = calculate_cart_total(cart_details)

    # Create order
    order = Order(
        ma_tai_khoan=user_id,
        tong_tien_tam_tinh=total,
        trang_thai=OrderStatus.PENDING
    )
    db.session.add(order)
    db.session.flush()  # Get order ID before creating details

    # Create order details
    for detail in cart_details:
        order_detail = OrderDetail(
            order_detail_id=order.ma_don_hang,
            product_id=detail.ma_san_pham,
            quantity=detail.so_luong,
            price=detail.gia_tai_thoi_diem,
            total_fee=float(detail.so_luong) * float(detail.gia_tai_thoi_diem),
        )
        db.session.add(order_detail)

    # Mark cart as completed
    cart.trang_thai = 1
    db.session.commit()

    return order


# -----------------------------------------------------------------------------
# Order Status Operations
# -----------------------------------------------------------------------------

def cancel_user_order(order: Order) -> bool:
    """Cancel an order (user-initiated).

    Only orders in PENDING or PROCESSING status can be cancelled by users.

    Args:
        order: The order to cancel.

    Returns:
        True if cancelled successfully, False if not cancellable.
    """
    if not OrderStatus.can_user_cancel(order.trang_thai):
        return False

    order.trang_thai = OrderStatus.CANCELLED
    db.session.commit()
    return True


# -----------------------------------------------------------------------------
# Purchase History
# -----------------------------------------------------------------------------

def get_order_details_with_products(order: Order) -> list[dict]:
    """Get order details with associated product information.

    Uses the existing relationship on Order model to get details,
    then fetches product info for each detail.

    Args:
        order: The order to get details for.

    Returns:
        List of dicts with 'detail' and 'product' keys.
    """
    result = []
    for detail in order.chi_tiet_don_hang:
        product = Product.query.get(detail.ma_san_pham)
        result.append({
            'detail': detail,
            'product': product
        })
    return result


def find_invoice_for_order(invoices: list[Invoice], order_id: int) -> Optional[Invoice]:
    """Find the matching invoice for an order from a list of invoices.

    Args:
        invoices: List of invoices to search.
        order_id: The order ID to match.

    Returns:
        Matching Invoice if found, None otherwise.
    """
    for invoice in invoices:
        if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang == order_id:
            return invoice
    return None


def build_purchase_history(orders: list[Order], invoices: list[Invoice]) -> list[dict]:
    """Build purchase history data structure for template rendering.

    Args:
        orders: List of completed orders.
        invoices: List of user's invoices.

    Returns:
        List of dicts with 'order', 'invoice', and 'details' keys.
    """
    history = []
    for order in orders:
        history.append({
            'order': order,
            'invoice': find_invoice_for_order(invoices, order.ma_don_hang),
            'details': get_order_details_with_products(order)
        })
    return history
