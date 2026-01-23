"""
Module route giỏ hàng người dùng.

Blueprint này xử lý các thao tác giỏ hàng phía người dùng bao gồm:
- Xem giỏ hàng
- Thêm sản phẩm vào giỏ
- Cập nhật số lượng sản phẩm
- Xóa sản phẩm khỏi giỏ
- Xóa toàn bộ giỏ hàng
- Trang thanh toán
"""

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.product import Product
from app.services.user_cart_service import (
    add_product_to_cart,
    build_cart_items_for_display,
    build_checkout_items,
    build_single_product_checkout,
    calculate_cart_totals,
    clear_cart_items,
    get_active_cart,
    get_cart_item,
    get_cart_item_count,
    get_cart_items,
    get_or_create_active_cart,
    paginate_items,
    remove_cart_item,
    update_cart_item_quantity,
    update_cart_modified_time,
)

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart",
)


# -----------------------------------------------------------------------------
# Xem giỏ hàng
# -----------------------------------------------------------------------------

@cart_bp.route("/", methods=["GET"])
@login_required
def show_cart_page():
    """Hiển thị trang giỏ hàng của người dùng.

    Hỗ trợ phân trang qua query param 'page'.

    Returns:
        Template được render với danh sách sản phẩm trong giỏ hàng.
    """
    cart = get_active_cart(current_user.ma_tai_khoan)

    cart_items_all = []
    total_price = 0.0

    if cart:
        items = get_cart_items(cart.ma_gio_hang)
        cart_items_all = build_cart_items_for_display(items)
        total_price, _ = calculate_cart_totals(items)

    # Phân trang
    page = int(request.args.get("page", 1))
    cart_items, pagination = paginate_items(cart_items_all, page)

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total_price=total_price,
        pagination=pagination,
        user=current_user,
    )


# -----------------------------------------------------------------------------
# Thêm sản phẩm vào giỏ
# -----------------------------------------------------------------------------

@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id: int):
    """Thêm sản phẩm vào giỏ hàng.

    Nếu sản phẩm đã có trong giỏ, tăng số lượng lên 1.
    Nếu giỏ hàng chưa tồn tại, tạo mới.

    Args:
        product_id: Mã sản phẩm cần thêm.

    Returns:
        Chuyển hướng đến trang giỏ hàng.
    """
    product = Product.query.get_or_404(product_id)
    cart = get_or_create_active_cart(current_user.ma_tai_khoan)

    add_product_to_cart(cart, product)

    return redirect(url_for("cart.show_cart_page"))


# -----------------------------------------------------------------------------
# Cập nhật số lượng sản phẩm
# -----------------------------------------------------------------------------

@cart_bp.route("/update/<int:id>/<action>")
@login_required
def update_cart(id: int, action: str):
    """Cập nhật số lượng sản phẩm trong giỏ hàng.

    Args:
        id: Mã sản phẩm cần cập nhật.
        action: Hành động ('increase' để tăng, 'decrease' để giảm).

    Returns:
        Chuyển hướng đến trang giỏ hàng.
    """
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        return redirect(url_for("cart.show_cart_page"))

    cart_item = get_cart_item(cart.ma_gio_hang, id)
    if cart_item is None:
        return redirect(url_for("cart.show_cart_page"))

    update_cart_item_quantity(cart_item, action)
    update_cart_modified_time(cart)
    db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


# -----------------------------------------------------------------------------
# Xóa sản phẩm khỏi giỏ
# -----------------------------------------------------------------------------

@cart_bp.route("/remove/<int:id>")
@login_required
def remove_cart(id: int):
    """Xóa sản phẩm khỏi giỏ hàng.

    Args:
        id: Mã sản phẩm cần xóa.

    Returns:
        Chuyển hướng đến trang giỏ hàng.
    """
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        return redirect(url_for("cart.show_cart_page"))

    cart_item = get_cart_item(cart.ma_gio_hang, id)
    if cart_item is None:
        return redirect(url_for("cart.show_cart_page"))

    remove_cart_item(cart_item)
    update_cart_modified_time(cart)
    db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


# -----------------------------------------------------------------------------
# Xóa toàn bộ giỏ hàng
# -----------------------------------------------------------------------------

@cart_bp.route("/clear")
@login_required
def clear_cart():
    """Xóa tất cả sản phẩm trong giỏ hàng.

    Returns:
        Chuyển hướng đến trang giỏ hàng.
    """
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        return redirect(url_for("cart.show_cart_page"))

    clear_cart_items(cart.ma_gio_hang)
    update_cart_modified_time(cart)
    db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


# -----------------------------------------------------------------------------
# Hàm tiện ích (exported cho các module khác)
# -----------------------------------------------------------------------------

def get_cart_count() -> int:
    """Lấy số lượng sản phẩm trong giỏ hàng của người dùng hiện tại.

    Hàm này được dùng cho việc hiển thị badge số lượng giỏ hàng.

    Returns:
        Số lượng sản phẩm trong giỏ hàng, 0 nếu chưa đăng nhập.
    """
    if not current_user.is_authenticated:
        return 0

    return get_cart_item_count(current_user.ma_tai_khoan)


# -----------------------------------------------------------------------------
# Trang thanh toán
# -----------------------------------------------------------------------------

@cart_bp.route("/checkouts", methods=["GET"])
@login_required
def show_checkout_page():
    """Hiển thị trang thanh toán.

    Nếu giỏ hàng trống hoặc không tồn tại, chuyển hướng về trang giỏ hàng.

    Returns:
        Template được render với thông tin thanh toán.
    """
    cart = get_active_cart(current_user.ma_tai_khoan)
    if cart is None:
        return redirect(url_for("cart.show_cart_page"))

    cart_details = get_cart_items(cart.ma_gio_hang)
    cart_items = build_checkout_items(cart_details)
    total_price, total_quantity = calculate_cart_totals(cart_details)

    return render_template(
        "checkouts.html",
        cart_items=cart_items,
        total_price=total_price,
        total_quantity=total_quantity,
        user=current_user,
    )


# -----------------------------------------------------------------------------
# Mua ngay (Buy Now)
# -----------------------------------------------------------------------------

@cart_bp.route("/buy-now/<int:product_id>", methods=["GET"])
@login_required
def buy_now(product_id: int):
    """Hiển thị trang thanh toán cho một sản phẩm cụ thể (Mua ngay).

    Cho phép người dùng mua trực tiếp một sản phẩm mà không cần thêm vào giỏ hàng.

    Args:
        product_id: Mã sản phẩm cần mua.

    Returns:
        Template được render với thông tin thanh toán cho sản phẩm đó.
    """
    product = Product.query.get_or_404(product_id)

    # Kiểm tra sản phẩm còn hàng không
    if product.so_luong <= 0:
        return redirect(url_for("main.show_home_page"))

    # Lấy số lượng từ query param (mặc định là 1)
    quantity = request.args.get("quantity", 1, type=int)
    if quantity < 1:
        quantity = 1
    if quantity > product.so_luong:
        quantity = product.so_luong

    cart_items, total_price, total_quantity = build_single_product_checkout(product, quantity)

    return render_template(
        "checkouts.html",
        cart_items=cart_items,
        total_price=total_price,
        total_quantity=total_quantity,
        user=current_user,
        buy_now_product_id=product_id,  # Đánh dấu đây là Buy Now
    )
