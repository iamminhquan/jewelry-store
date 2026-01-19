from app.models.product import Product


def get_all_products():
    return Product.query.all()
