from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_login import current_user, login_required

from app.models.product import Product
from app.services.user_product_service import get_related_products
from app.services.favorite_service import (
    is_product_favorited,
    toggle_favorite,
)

user_product_bp = Blueprint(
    "user_product",
    __name__,
    url_prefix="/product",
)


@user_product_bp.route("/<int:product_id>", methods=["GET"])
def show_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = get_related_products(product)

    # Kiểm tra sản phẩm đã được yêu thích chưa
    is_favorited = False
    if current_user.is_authenticated:
        is_favorited = is_product_favorited(current_user.ma_tai_khoan, product_id)

    return render_template(
        "user/product_detail.html",
        product=product,
        related_products=related_products,
        is_favorited=is_favorited,
    )


@user_product_bp.route("/favorite/<int:product_id>", methods=["POST"])
@login_required
def toggle_favorite_product(product_id):
    """Toggle trạng thái yêu thích của sản phẩm."""
    product = Product.query.get_or_404(product_id)
    result = toggle_favorite(current_user.ma_tai_khoan, product_id)

    # Nếu là AJAX request, trả về JSON
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(result)

    # Nếu không, redirect về trang trước
    return redirect(request.referrer or url_for("main.show_home_page"))
