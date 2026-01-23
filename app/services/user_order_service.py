"""
Module service đơn hàng người dùng.

Module này cung cấp logic nghiệp vụ cho các thao tác đơn hàng phía người dùng,
tách biệt với các thao tác đơn hàng admin trong order_service.py.
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
# Hàm hỗ trợ truy vấn
# -----------------------------------------------------------------------------

def get_user_orders(user_id: int) -> list[Order]:
    """Lấy tất cả đơn hàng của người dùng, sắp xếp theo ngày tạo giảm dần.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Danh sách đối tượng Order thuộc về người dùng.
    """
    return (
        Order.query
        .filter_by(ma_tai_khoan=user_id)
        .order_by(Order.ngay_tao.desc())
        .all()
    )


def get_user_order_or_none(order_id: int, user_id: int) -> Optional[Order]:
    """Lấy đơn hàng thuộc về một người dùng cụ thể.

    Args:
        order_id: Mã đơn hàng cần lấy.
        user_id: Mã tài khoản người dùng (để xác thực quyền sở hữu).

    Returns:
        Order nếu tìm thấy và thuộc về người dùng, None nếu không.
    """
    return Order.query.filter_by(
        ma_don_hang=order_id,
        ma_tai_khoan=user_id
    ).first()


def get_user_completed_orders(user_id: int) -> list[Order]:
    """Lấy tất cả đơn hàng đã hoàn thành của người dùng.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Danh sách đối tượng Order đã hoàn thành, sắp xếp theo ngày tạo giảm dần.
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
    """Lấy giỏ hàng đang hoạt động (chưa hoàn thành) của người dùng.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Cart đang hoạt động nếu tìm thấy, None nếu không.
    """
    return Cart.query.filter_by(
        ma_tai_khoan=user_id,
        trang_thai=0
    ).first()


def get_cart_details(cart_id: int) -> list[CartDetail]:
    """Lấy tất cả chi tiết giỏ hàng của một giỏ hàng.

    Args:
        cart_id: Mã giỏ hàng.

    Returns:
        Danh sách đối tượng CartDetail.
    """
    return CartDetail.query.filter_by(ma_gio_hang=cart_id).all()


def get_user_invoice_or_none(invoice_id: int, user_id: int) -> Optional[Invoice]:
    """Lấy hóa đơn thuộc về một người dùng cụ thể.

    Args:
        invoice_id: Mã hóa đơn cần lấy.
        user_id: Mã tài khoản người dùng (để xác thực quyền sở hữu).

    Returns:
        Invoice nếu tìm thấy và thuộc về người dùng, None nếu không.
    """
    return Invoice.query.filter_by(
        ma_hoa_don=invoice_id,
        ma_tai_khoan=user_id
    ).first()


def get_related_order(invoice: Invoice) -> Optional[Order]:
    """Lấy đơn hàng liên quan đến hóa đơn nếu tồn tại.

    Args:
        invoice: Đối tượng hóa đơn.

    Returns:
        Order nếu tìm thấy và hóa đơn có ma_don_hang, None nếu không.
    """
    if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang:
        return Order.query.get(invoice.ma_don_hang)
    return None


# -----------------------------------------------------------------------------
# Tạo đơn hàng
# -----------------------------------------------------------------------------

def calculate_cart_total(cart_details: list[CartDetail]) -> float:
    """Tính tổng tiền từ chi tiết giỏ hàng.

    Args:
        cart_details: Danh sách đối tượng CartDetail.

    Returns:
        Tổng tiền dạng float.
    """
    return sum(
        float(detail.so_luong) * float(detail.gia_tai_thoi_diem)
        for detail in cart_details
    )


def create_order_from_cart(user_id: int, cart: Cart, cart_details: list[CartDetail]) -> Order:
    """Tạo đơn hàng mới từ nội dung giỏ hàng.

    Hàm này thực hiện:
    1. Tạo đơn hàng với trạng thái chờ xử lý
    2. Tạo chi tiết đơn hàng từ chi tiết giỏ hàng
    3. Đánh dấu giỏ hàng là đã hoàn thành (trang_thai=1)

    Args:
        user_id: Mã tài khoản người dùng.
        cart: Giỏ hàng cần chuyển đổi.
        cart_details: Các sản phẩm trong giỏ hàng.

    Returns:
        Đơn hàng vừa được tạo.
    """
    total = calculate_cart_total(cart_details)

    # Tạo đơn hàng
    order = Order(
        ma_tai_khoan=user_id,
        tong_tien_tam_tinh=total,
        trang_thai=OrderStatus.PENDING
    )
    db.session.add(order)
    db.session.flush()  # Lấy mã đơn hàng trước khi tạo chi tiết

    # Tạo chi tiết đơn hàng
    for detail in cart_details:
        order_detail = OrderDetail(
            order_detail_id=order.ma_don_hang,
            product_id=detail.ma_san_pham,
            quantity=detail.so_luong,
            price=detail.gia_tai_thoi_diem,
            total_fee=float(detail.so_luong) * float(detail.gia_tai_thoi_diem),
        )
        db.session.add(order_detail)

    # Đánh dấu giỏ hàng đã hoàn thành
    cart.trang_thai = 1
    db.session.commit()

    return order


def create_order_from_product(user_id: int, product: Product, quantity: int = 1) -> Order:
    """Tạo đơn hàng mới từ một sản phẩm (Buy Now).

    Hàm này thực hiện:
    1. Tạo đơn hàng với trạng thái chờ xử lý
    2. Tạo chi tiết đơn hàng từ sản phẩm được chọn

    Args:
        user_id: Mã tài khoản người dùng.
        product: Sản phẩm cần mua.
        quantity: Số lượng sản phẩm (mặc định là 1).

    Returns:
        Đơn hàng vừa được tạo.
    """
    total = float(product.gia_xuat) * quantity

    # Tạo đơn hàng
    order = Order(
        ma_tai_khoan=user_id,
        tong_tien_tam_tinh=total,
        trang_thai=OrderStatus.PENDING
    )
    db.session.add(order)
    db.session.flush()  # Lấy mã đơn hàng trước khi tạo chi tiết

    # Tạo chi tiết đơn hàng
    order_detail = OrderDetail(
        order_detail_id=order.ma_don_hang,
        product_id=product.ma_san_pham,
        quantity=quantity,
        price=product.gia_xuat,
        total_fee=total,
    )
    db.session.add(order_detail)
    db.session.commit()

    return order


# -----------------------------------------------------------------------------
# Thao tác trạng thái đơn hàng
# -----------------------------------------------------------------------------

def cancel_user_order(order: Order) -> bool:
    """Hủy đơn hàng (do người dùng thực hiện).

    Chỉ đơn hàng ở trạng thái CHỜ XỬ LÝ hoặc ĐANG XỬ LÝ mới có thể
    được hủy bởi người dùng.

    Args:
        order: Đơn hàng cần hủy.

    Returns:
        True nếu hủy thành công, False nếu không thể hủy.
    """
    if not OrderStatus.can_user_cancel(order.trang_thai):
        return False

    order.trang_thai = OrderStatus.CANCELLED
    db.session.commit()
    return True


# -----------------------------------------------------------------------------
# Lịch sử mua hàng
# -----------------------------------------------------------------------------

def get_order_details_with_products(order: Order) -> list[dict]:
    """Lấy chi tiết đơn hàng kèm thông tin sản phẩm liên quan.

    Sử dụng relationship có sẵn trên model Order để lấy chi tiết,
    sau đó lấy thông tin sản phẩm cho từng chi tiết.

    Args:
        order: Đơn hàng cần lấy chi tiết.

    Returns:
        Danh sách dict với các key 'detail' và 'product'.
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
    """Tìm hóa đơn tương ứng với đơn hàng từ danh sách hóa đơn.

    Args:
        invoices: Danh sách hóa đơn cần tìm kiếm.
        order_id: Mã đơn hàng cần khớp.

    Returns:
        Invoice khớp nếu tìm thấy, None nếu không.
    """
    for invoice in invoices:
        if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang == order_id:
            return invoice
    return None


def build_purchase_history(orders: list[Order], invoices: list[Invoice]) -> list[dict]:
    """Xây dựng cấu trúc dữ liệu lịch sử mua hàng để render template.

    Args:
        orders: Danh sách đơn hàng đã hoàn thành.
        invoices: Danh sách hóa đơn của người dùng.

    Returns:
        Danh sách dict với các key 'order', 'invoice', và 'details'.
    """
    history = []
    for order in orders:
        history.append({
            'order': order,
            'invoice': find_invoice_for_order(invoices, order.ma_don_hang),
            'details': get_order_details_with_products(order)
        })
    return history
