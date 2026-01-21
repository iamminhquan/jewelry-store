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


def get_products_by_id(product_id):
    """Lấy danh sách sản phẩm dựa trên danh sách mã sản phẩm.

    Args:
        product_ids (list): Danh sách mã sản phẩm.

    Returns:
        list: Danh sách sản phẩm tương ứng với mã sản phẩm đã cho.
    """
    products = Product.query.filter(Product.ma_san_pham.in_(product_id)).all()
    return products


def check_status(product):
    if product.so_luong > 0:
        return "IN_STOCK"

    return "OUT_OF_STOCK"
