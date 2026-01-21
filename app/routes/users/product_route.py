from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models.product import Product

user_product_bp = Blueprint(
    "user_product",
    __name__,
    url_prefix="/product",
)


@user_product_bp.route("/<int:product_id>", methods=["GET"])
def show_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("user/product_detail.html", product=product)
