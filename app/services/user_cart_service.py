"""
Module service giỏ hàng người dùng.

Module này cung cấp logic nghiệp vụ cho các thao tác giỏ hàng phía người dùng,
bao gồm lấy giỏ hàng, tính toán tổng tiền, và phân trang.
"""

import math
from datetime import datetime
from typing import Optional

from app.extensions import db
from app.models.cart import Cart
from app.models.cart_detail import CartDetail
from app.models.product import Product


# -----------------------------------------------------------------------------
# Hằng số
# -----------------------------------------------------------------------------

CART_STATUS_ACTIVE = 0
CART_STATUS_COMPLETED = 1
CART_ITEMS_PER_PAGE = 5


# -----------------------------------------------------------------------------
# Hàm hỗ trợ truy vấn giỏ hàng
# -----------------------------------------------------------------------------

def get_active_cart(user_id: int) -> Optional[Cart]:
    """Lấy giỏ hàng đang hoạt động của người dùng.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Cart đang hoạt động nếu tìm thấy, None nếu không.
    """
    return Cart.query.filter_by(
        ma_tai_khoan=user_id,
        trang_thai=CART_STATUS_ACTIVE
    ).first()


def get_or_create_active_cart(user_id: int) -> Cart:
    """Lấy giỏ hàng đang hoạt động hoặc tạo mới nếu chưa có.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Cart đang hoạt động (có thể mới được tạo).
    """
    cart = get_active_cart(user_id)

    if cart is None:
        cart = Cart(
            account_id=user_id,
            created_at=datetime.utcnow(),
            status=CART_STATUS_ACTIVE,
        )
        db.session.add(cart)
        db.session.commit()

    return cart


def get_cart_items(cart_id: int) -> list[CartDetail]:
    """Lấy tất cả sản phẩm trong giỏ hàng.

    Args:
        cart_id: Mã giỏ hàng.

    Returns:
        Danh sách đối tượng CartDetail.
    """
    return CartDetail.query.filter_by(ma_gio_hang=cart_id).all()


def get_cart_item(cart_id: int, product_id: int) -> Optional[CartDetail]:
    """Lấy một sản phẩm cụ thể trong giỏ hàng.

    Args:
        cart_id: Mã giỏ hàng.
        product_id: Mã sản phẩm.

    Returns:
        CartDetail nếu tìm thấy, None nếu không.
    """
    return CartDetail.query.filter_by(
        ma_gio_hang=cart_id,
        ma_san_pham=product_id
    ).first()


def get_cart_item_count(user_id: int) -> int:
    """Đếm số lượng sản phẩm trong giỏ hàng của người dùng.

    Args:
        user_id: Mã tài khoản người dùng.

    Returns:
        Số lượng sản phẩm trong giỏ hàng.
    """
    cart = get_active_cart(user_id)

    if cart is None:
        return 0

    return CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).count()


# -----------------------------------------------------------------------------
# Tính toán giỏ hàng
# -----------------------------------------------------------------------------

def calculate_cart_totals(cart_items: list[CartDetail]) -> tuple[float, int]:
    """Tính tổng tiền và tổng số lượng sản phẩm trong giỏ hàng.

    Args:
        cart_items: Danh sách chi tiết giỏ hàng.

    Returns:
        Tuple gồm (tổng tiền, tổng số lượng).
    """
    total_price = 0.0
    total_quantity = 0

    for item in cart_items:
        total_price += item.so_luong * float(item.gia_tai_thoi_diem)
        total_quantity += item.so_luong

    return total_price, total_quantity


def build_cart_items_for_display(cart_items: list[CartDetail]) -> list[dict]:
    """Xây dựng danh sách sản phẩm giỏ hàng để hiển thị trên trang giỏ hàng.

    Args:
        cart_items: Danh sách chi tiết giỏ hàng.

    Returns:
        Danh sách dict chứa thông tin hiển thị cơ bản.
    """
    result = []
    for item in cart_items:
        product = Product.query.get(item.ma_san_pham)

        if product is None:
            continue

        # Lấy ảnh chính hoặc ảnh đầu tiên nếu có
        image_url = None
        if product.hinh_anhs:
            main_imgs = [img for img in product.hinh_anhs if img.anh_chinh == 1]
            if main_imgs:
                image_url = main_imgs[0].duong_dan
            else:
                image_url = product.hinh_anhs[0].duong_dan

        result.append({
            "id": item.ma_san_pham,
            "name": product.ten_san_pham,
            "quantity": item.so_luong,
            "price": float(item.gia_tai_thoi_diem),
            "image": f"/static/{image_url}" if image_url else "",
        })
    return result


def build_checkout_items(cart_items: list[CartDetail]) -> list[dict]:
    """Xây dựng danh sách sản phẩm để hiển thị trên trang thanh toán.

    Bao gồm thông tin chi tiết sản phẩm như tên và hình ảnh.

    Args:
        cart_items: Danh sách chi tiết giỏ hàng.

    Returns:
        Danh sách dict chứa thông tin đầy đủ cho trang checkout.
    """
    result = []

    for cart_detail in cart_items:
        product = Product.query.get(cart_detail.ma_san_pham)

        if product is None:
            continue

        # Lấy ảnh đầu tiên nếu có
        image_url = None
        if product.hinh_anhs:
            image_url = product.hinh_anhs[0].duong_dan

        result.append({
            "id": product.ma_san_pham,
            "name": product.ten_san_pham,
            "price": float(cart_detail.gia_tai_thoi_diem),
            "quantity": cart_detail.so_luong,
            "image": image_url,
        })

    return result


def build_single_product_checkout(product: Product, quantity: int = 1) -> tuple[list[dict], float, int]:
    """Xây dựng thông tin checkout cho một sản phẩm đơn lẻ (Buy Now).

    Args:
        product: Sản phẩm cần mua ngay.
        quantity: Số lượng sản phẩm (mặc định là 1).

    Returns:
        Tuple gồm (danh sách cart_items, tổng tiền, tổng số lượng).
    """
    # Lấy ảnh đầu tiên nếu có
    image_url = None
    if product.hinh_anhs:
        image_url = product.hinh_anhs[0].duong_dan

    cart_items = [{
        "id": product.ma_san_pham,
        "name": product.ten_san_pham,
        "price": float(product.gia_xuat),
        "quantity": quantity,
        "image": image_url,
    }]

    total_price = float(product.gia_xuat) * quantity
    total_quantity = quantity

    return cart_items, total_price, total_quantity


# -----------------------------------------------------------------------------
# Phân trang
# -----------------------------------------------------------------------------

def paginate_items(items: list, page: int, per_page: int = CART_ITEMS_PER_PAGE) -> tuple[list, dict]:
    """Phân trang danh sách items.

    Args:
        items: Danh sách cần phân trang.
        page: Số trang hiện tại (bắt đầu từ 1).
        per_page: Số items mỗi trang.

    Returns:
        Tuple gồm (danh sách items của trang hiện tại, dict thông tin phân trang).
    """
    total_items = len(items)
    total_pages = math.ceil(total_items / per_page) if total_items else 1

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_items = items[start_index:end_index]

    pagination = {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

    return paginated_items, pagination


# -----------------------------------------------------------------------------
# Thao tác giỏ hàng
# -----------------------------------------------------------------------------

def add_product_to_cart(cart: Cart, product: Product) -> CartDetail:
    """Thêm sản phẩm vào giỏ hàng.

    Nếu sản phẩm đã có trong giỏ, tăng số lượng lên 1.
    Nếu chưa có, tạo mới chi tiết giỏ hàng.

    Args:
        cart: Giỏ hàng.
        product: Sản phẩm cần thêm.

    Returns:
        CartDetail đã được thêm hoặc cập nhật.
    """
    cart_item = get_cart_item(cart.ma_gio_hang, product.ma_san_pham)

    if cart_item:
        cart_item.so_luong += 1
    else:
        cart_item = CartDetail(
            cart_detail_id=cart.ma_gio_hang,
            product_id=product.ma_san_pham,
            quantity=1,
            price_at=product.gia_xuat,
            created_at=datetime.utcnow(),
        )
        db.session.add(cart_item)

    update_cart_modified_time(cart)
    db.session.commit()

    return cart_item


def update_cart_item_quantity(cart_item: CartDetail, action: str) -> bool:
    """Cập nhật số lượng sản phẩm trong giỏ hàng.

    Args:
        cart_item: Chi tiết giỏ hàng cần cập nhật.
        action: Hành động ('increase' hoặc 'decrease').

    Returns:
        True nếu item vẫn tồn tại, False nếu đã bị xóa.
    """
    if action == "increase":
        cart_item.so_luong += 1
        return True

    if action == "decrease":
        cart_item.so_luong -= 1
        if cart_item.so_luong <= 0:
            db.session.delete(cart_item)
            return False

    return True


def remove_cart_item(cart_item: CartDetail) -> None:
    """Xóa sản phẩm khỏi giỏ hàng.

    Args:
        cart_item: Chi tiết giỏ hàng cần xóa.
    """
    db.session.delete(cart_item)


def clear_cart_items(cart_id: int) -> None:
    """Xóa tất cả sản phẩm trong giỏ hàng.

    Args:
        cart_id: Mã giỏ hàng.
    """
    CartDetail.query.filter_by(ma_gio_hang=cart_id).delete()


def update_cart_modified_time(cart: Cart) -> None:
    """Cập nhật thời gian chỉnh sửa của giỏ hàng.

    Args:
        cart: Giỏ hàng cần cập nhật.
    """
    cart.ngay_chinh_sua = datetime.utcnow()
