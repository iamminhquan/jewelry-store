from flask import Blueprint, abort, redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.invoice import Invoice
from app.models.product import Product
from app.extensions import db
from app.models.cart import Cart
from app.models.cart_detail import CartDetail
from app.constants import OrderStatus
from app.services.invoice_service import get_invoices_by_user
from app.services.invoice_detail_service import get_invoice_detail_with_product

user_order_bp = Blueprint(
    "user_order",
    __name__,
    url_prefix="/order",
)


@user_order_bp.route("/", methods=["GET"])
@login_required
def show_orders():
    """Display all orders for the current user.
    
    Returns:
        Response: Template with user's orders list.
    """
    orders = Order.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan
    ).order_by(Order.ngay_tao.desc()).all()

    return render_template(
        "user/orders.html", 
        orders=orders,
        OrderStatus=OrderStatus
    )


@user_order_bp.route("/", methods=["POST"])
@login_required
def create_order():
    full_name = request.form.get("full_name")
    phone = request.form.get("phone")
    address = request.form.get("address")
    payment_method = request.form.get("payment_method")

    if not full_name or not phone or not address:
        abort(400)

    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first_or_404()

    cart_details = CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).all()

    if not cart_details:
        abort(400)

    tong_tien = sum(d.so_luong * d.gia_tai_thoi_diem for d in cart_details)

    order = Order(
        ma_tai_khoan=current_user.ma_tai_khoan,
        tong_tien_tam_tinh=tong_tien,
        trang_thai=OrderStatus.PENDING
    )
    db.session.add(order)
    db.session.flush()

    for d in cart_details:
        db.session.add(
            OrderDetail(
                order_detail_id=order.ma_don_hang,
                product_id=d.ma_san_pham,
                quantity=d.so_luong,
                price=d.gia_tai_thoi_diem,
                total_fee=d.so_luong * d.gia_tai_thoi_diem,
            )
        )

    cart.trang_thai = 1
    db.session.commit()

    return redirect(url_for("user_order.show_order_detail", order_id=order.ma_don_hang))


@user_order_bp.route("/<int:order_id>")
@login_required
def show_order_detail(order_id):
    """Display order detail for the current user.
    
    Args:
        order_id (int): The order ID to display.
        
    Returns:
        Response: Template with order details.
    """
    order = Order.query.filter_by(
        ma_don_hang=order_id, ma_tai_khoan=current_user.ma_tai_khoan
    ).first_or_404()

    return render_template(
        "user/order.html", 
        order=order,
        OrderStatus=OrderStatus
    )


@user_order_bp.route("/<int:order_id>/cancel", methods=["POST"])
@login_required
def cancel_order(order_id):
    """Cancel an order (user-initiated).
    
    Users can only cancel their own orders that are in Pending or Processing status.
    
    Args:
        order_id (int): The order ID to cancel.
        
    Returns:
        Response: Redirect to orders page with flash message.
    """
    # Get order and verify ownership
    order = Order.query.filter_by(
        ma_don_hang=order_id, 
        ma_tai_khoan=current_user.ma_tai_khoan
    ).first_or_404()
    
    # Check if order can be cancelled
    if not OrderStatus.can_user_cancel(order.trang_thai):
        flash("Không thể hủy đơn hàng này. Đơn hàng đang được giao hoặc đã hoàn thành.", "error")
        return redirect(url_for("user_order.show_orders"))
    
    # Cancel the order
    order.trang_thai = OrderStatus.CANCELLED
    db.session.commit()
    
    flash("Đơn hàng đã được hủy thành công.", "success")
    return redirect(url_for("user_order.show_orders"))


@user_order_bp.route("/purchase-history")
@login_required
def show_purchase_history():
    """Display purchase history (completed orders with invoices) for the current user.
    
    Returns:
        Response: Template with user's purchase history.
    """
    # Get completed orders for the user
    completed_orders = Order.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan,
        trang_thai=OrderStatus.COMPLETED
    ).order_by(Order.ngay_tao.desc()).all()
    
    # Get invoices for the user
    invoices = get_invoices_by_user(current_user.ma_tai_khoan)
    
    # Build purchase history with order details and product info
    purchase_history = []
    for order in completed_orders:
        order_details_with_products = []
        for detail in order.chi_tiet_don_hang:
            product = Product.query.get(detail.ma_san_pham)
            order_details_with_products.append({
                'detail': detail,
                'product': product
            })
        
        # Find matching invoice if any
        matching_invoice = None
        for invoice in invoices:
            try:
                if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang == order.ma_don_hang:
                    matching_invoice = invoice
                    break
            except Exception:
                pass
        
        purchase_history.append({
            'order': order,
            'invoice': matching_invoice,
            'details': order_details_with_products
        })
    
    return render_template(
        "user/purchase_history.html",
        purchase_history=purchase_history,
        OrderStatus=OrderStatus
    )


@user_order_bp.route("/invoice/<int:invoice_id>")
@login_required
def show_invoice_detail(invoice_id):
    """Display invoice detail for the current user.
    
    Args:
        invoice_id (int): The invoice ID to display.
        
    Returns:
        Response: Template with invoice details.
    """
    # Get invoice and verify ownership
    invoice = Invoice.query.filter_by(
        ma_hoa_don=invoice_id,
        ma_tai_khoan=current_user.ma_tai_khoan
    ).first_or_404()
    
    # Get invoice details with product info
    invoice_details = get_invoice_detail_with_product(invoice_id)
    
    # Get related order if exists
    order = None
    try:
        if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang:
            order = Order.query.get(invoice.ma_don_hang)
    except Exception:
        pass
    
    return render_template(
        "user/invoice_detail.html",
        invoice=invoice,
        order=order,
        invoice_details=invoice_details,
        OrderStatus=OrderStatus
    )
