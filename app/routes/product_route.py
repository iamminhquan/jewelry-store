from flask import Blueprint, render_template


from app.services.product_service import get_all_products

product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/products",
)


@product_bp.route("/", methods=["GET"])
def show_all_products():
    products = get_all_products()

    return render_template(
        "product/index.html",
        products=products,
    )
