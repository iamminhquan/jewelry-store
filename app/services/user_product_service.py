from typing import List, Optional

from app.models.product import Product
from app.models.product_image import ProductImage


def get_product_images(product_id: int) -> List[str]:
    """Lấy tất cả hình ảnh của sản phẩm theo ID.

    Câu truy vấn tương đương:
    `SELECT duong_dan`
    `FROM hinhanhsanpham`
    `WHERE ma_san_pham = :product_id`
    `ORDER BY anh_chinh DESC, thu_tu_sap_xep ASC`

    :params: product_id (int): Mã sản phẩm cần lấy hình ảnh.

    Returns:
        List[str]: Danh sách đường dẫn hình ảnh.
    """
    images = (
        ProductImage.query.filter(ProductImage.ma_san_pham == product_id)
        .order_by(
            ProductImage.anh_chinh.desc(),  # Ảnh chính lên đầu
            ProductImage.thu_tu_sap_xep.asc(),
        )
        .all()
    )
    return [img.duong_dan for img in images]


def get_main_product_image(product_id: int) -> Optional[str]:
    """Lấy hình ảnh chính của sản phẩm theo ID.

    Ưu tiên: ảnh có anh_chinh=1 > ảnh đầu tiên theo thứ tự

    Args:
        product_id (int): Mã sản phẩm.

    Returns:
        Optional[str]: Đường dẫn hình ảnh chính hoặc None nếu không có.
    """
    # Tìm ảnh chính trước
    main_image = ProductImage.query.filter(
        ProductImage.ma_san_pham == product_id, ProductImage.anh_chinh == 1
    ).first()

    if main_image:
        return main_image.duong_dan

    # Nếu không có ảnh chính, lấy ảnh đầu tiên
    first_image = (
        ProductImage.query.filter(ProductImage.ma_san_pham == product_id)
        .order_by(ProductImage.thu_tu_sap_xep.asc())
        .first()
    )

    return first_image.duong_dan if first_image else None


def get_product_with_images(product_id: int):
    """Lấy sản phẩm kèm theo hình ảnh.

    Args:
        product_id (int): Mã sản phẩm.

    Returns:
        tuple: (Product, List[str]) - Sản phẩm và danh sách đường dẫn hình ảnh.
    """
    product = Product.query.get(product_id)
    if not product:
        return None, []

    images = get_product_images(product_id)
    return product, images


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
