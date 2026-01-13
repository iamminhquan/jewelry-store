from flask import Blueprint, render_template
from app.models.product import Products


product_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
)


@product_bp.route("/")
def show_all_products():
    products = Products.query.all()

    return render_template(
        "product/index.html",
        products=products,
    )
