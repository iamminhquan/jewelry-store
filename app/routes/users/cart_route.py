from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from app.models.product import Product
from app.models.cart import Cart
from app.models.cart_detail import CartDetail
from app.extensions import db
from datetime import datetime
import math

cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart",
)


@cart_bp.route("/", methods=["GET"])
@login_required
def show_cart_page():
    # Lấy giỏ hàng từ Database.
    if not current_user.is_authenticated:
        return "1"

    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    cart_items_all = []
    total_price = 0

    if cart:
        items = CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).all()

        for item in items:
            cart_items_all.append(
                {
                    "id": item.ma_san_pham,
                    "quantity": item.so_luong,
                    "price": float(item.gia_tai_thoi_diem),
                }
            )
            total_price += item.so_luong * float(item.gia_tai_thoi_diem)

    # Phân trang.
    PER_PAGE = 5
    page = int(request.args.get("page", 1))

    total_items = len(cart_items_all)
    total_pages = math.ceil(total_items / PER_PAGE) if total_items else 1

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    cart_items = cart_items_all[start:end]

    pagination = {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

    # Kết xuất ra giao diện.
    return render_template(
        "cart.html",
        cart_items=cart_items,
        total_price=total_price,
        pagination=pagination,
        user=current_user,
    )


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    # Lấy giỏ hàng hiện tại đang sử dụng.
    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    if not cart:
        cart = Cart(
            account_id=current_user.ma_tai_khoan,
            created_at=datetime.utcnow(),
            status=0,
        )
        db.session.add(cart)
        db.session.commit()  # để có ma_gio_hang

    # Kiểm tra sản phẩm trong giỏ hàng
    cart_item = CartDetail.query.filter_by(
        ma_gio_hang=cart.ma_gio_hang, ma_san_pham=product.ma_san_pham
    ).first()

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

    cart.ngay_chinh_sua = datetime.utcnow()
    db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


@cart_bp.route("/cart/update/<int:id>/<action>")
@login_required
def update_cart(id, action):
    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    if not cart:
        return redirect(url_for("cart.show_cart_page"))

    item = CartDetail.query.filter_by(
        ma_gio_hang=cart.ma_gio_hang, ma_san_pham=id
    ).first()

    if not item:
        return redirect(url_for("cart.show_cart_page"))

    if action == "increase":
        item.so_luong += 1

    elif action == "decrease":
        item.so_luong -= 1
        if item.so_luong <= 0:
            db.session.delete(item)

    cart.ngay_chinh_sua = datetime.utcnow()
    db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


@cart_bp.route("/cart/remove/<int:id>")
@login_required
def remove_cart(id):
    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    if not cart:
        return redirect(url_for("cart.show_cart_page"))

    item = CartDetail.query.filter_by(
        ma_gio_hang=cart.ma_gio_hang, ma_san_pham=id
    ).first()

    if item:
        db.session.delete(item)
        cart.ngay_chinh_sua = datetime.utcnow()
        db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


@cart_bp.route("/cart/clear")
@login_required
def clear_cart():
    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    if cart:
        CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).delete()

        cart.ngay_chinh_sua = datetime.utcnow()
        db.session.commit()

    return redirect(url_for("cart.show_cart_page"))


def get_cart_count():
    if not current_user.is_authenticated:
        return 0

    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan, trang_thai=0
    ).first()

    if not cart:
        return 0

    return CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).count()


@cart_bp.route("/checkouts", methods=["GET"])
@login_required
def show_checkout_page():
    cart = Cart.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan,
        trang_thai=0,
    ).first()

    if not cart:
        return redirect(url_for("cart.show_cart_page"))

    cart_details = CartDetail.query.filter_by(ma_gio_hang=cart.ma_gio_hang).all()

    cart_items = []
    total_price = 0
    total_quantity = 0

    for d in cart_details:
        product = Product.query.filter_by(ma_san_pham=d.ma_san_pham).first()

        if not product:
            continue

        # Lấy ảnh đầu tiên (nếu có).
        image_url = None
        if product.hinh_anhs:
            image_url = product.hinh_anhs[0].duong_dan

        item_total = d.so_luong * d.gia_tai_thoi_diem

        cart_items.append(
            {
                "id": product.ma_san_pham,
                "name": product.ten_san_pham,
                "price": float(d.gia_tai_thoi_diem),
                "quantity": d.so_luong,
                "image": image_url,
            }
        )

        total_price += item_total
        total_quantity += d.so_luong

    return render_template(
        "checkouts.html",
        cart_items=cart_items,
        total_price=total_price,
        total_quantity=total_quantity,
        user=current_user,
    )
