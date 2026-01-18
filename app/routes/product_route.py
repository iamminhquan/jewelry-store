from flask import Blueprint, render_template
from sqlalchemy import select

from app.models.product import Product
from app.models.product_image import ProductImage
from app.extensions import db


product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/products",
)


@product_bp.route("/", methods=["GET"])
def show_all_products():
    products = Product.query.all()

    return render_template(
        "product/index.html",
        products=products,
    )


@product_bp.route("/images", methods=["GET"])
def show_all_images():
    product_images = (
        db.session.execute(
            select(ProductImage.duong_dan)
            .join(Product)
            .where(Product.ma_san_pham == ProductImage.ma_san_pham)
        )
        .scalars()
        .all()
    )

    return render_template(
        "product/images.html",
        product_images=product_images,
    )
