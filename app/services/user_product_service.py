from app.models.product import Product


def get_best_seller_products(limit: int = 5):
    """Lấy danh sách sản phẩm bán chạy nhất.

    Args:
        limit (int, optional): Số lượng sản phẩm cần lấy. Mặc định là 5.

    Returns:
        list: Danh sách sản phẩm bán chạy nhất.
    """
    best_sellers = (
        Product.query.filter(Product.trang_thai == 1)
        .order_by(Product.so_luong.desc())
        .limit(limit)
        .all()
    )
    return best_sellers


def get_new_products(limit: int = 5):
    """Lấy danh sách sản phẩm mới nhất.

    Args:
        limit (int, optional): Số lượng sản phẩm cần lấy. Mặc định là 5.

    Returns:
        list: Danh sách sản phẩm mới nhất.
    """
    new_products = (
        Product.query.filter(Product.trang_thai == 1)
        .order_by(Product.ngay_tao.desc())
        .limit(limit)
        .all()
    )
    return new_products

def get_related_products(product, limit=5):
    related_products = (
        Product.query.filter(
            Product.trang_thai == 1,
            Product.ma_san_pham != product.ma_san_pham,
            Product.gioi_tinh == product.gioi_tinh,
        )
        .order_by(Product.ngay_tao.desc())
        .limit(limit)
        .all()
    )
    return related_products