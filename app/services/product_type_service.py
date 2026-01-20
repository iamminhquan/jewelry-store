from app.extensions import db
from app.models.product_type import ProductType
from app.models.category import Category
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_product_type_query(keyword: str, ma_danh_muc: str):
    """Tạo truy vấn loại sản phẩm theo từ khoá và danh mục.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        ma_danh_muc (str): Mã danh mục lọc (hoặc None).

    Returns:
        BaseQuery: Truy vấn loại sản phẩm đã áp dụng điều kiện lọc.
    """
    query = ProductType.query

    if ma_danh_muc:
        try:
            ma_danh_muc_int = int(ma_danh_muc)
            query = query.filter(ProductType.ma_danh_muc == ma_danh_muc_int)
        except (TypeError, ValueError):
            pass

    if keyword:
        query = query.filter(
            or_(
                cast(ProductType.ma_loai_san_pham, String).like(f"%{keyword}%"),
                ProductType.ten_loai_san_pham.ilike(f"%{keyword}%"),
                ProductType.slug.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_product_type_page(keyword: str, ma_danh_muc: str, page: int, per_page: int = 3):
    """Lấy dữ liệu loại sản phẩm theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        ma_danh_muc (str): Mã danh mục lọc (hoặc None).
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, product_types, total_product_types, ten_lsp_noi_bat)
    """
    query = build_product_type_query(keyword, ma_danh_muc)

    pagination = query.order_by(ProductType.ma_loai_san_pham.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_product_types = ProductType.query.count()

    loai_san_pham_noi_bat = ProductType.query.limit(3).all()
    ten_lsp_noi_bat = ", ".join(lsp.ten_loai_san_pham for lsp in loai_san_pham_noi_bat)

    return (
        pagination,
        pagination.items,
        total_product_types,
        ten_lsp_noi_bat,
    )


def get_product_type_or_404(product_type_id: int):
    """Lấy loại sản phẩm theo id hoặc trả về 404.

    Args:
        product_type_id (int): Mã loại sản phẩm.

    Returns:
        ProductType: Loại sản phẩm tìm thấy.
    """
    return ProductType.query.get_or_404(product_type_id)


def get_all_categories():
    """Lấy tất cả danh mục để hiển thị trong form.

    Returns:
        list: Danh sách tất cả danh mục.
    """
    return Category.query.filter(Category.trang_thai != 3).all()


def create_product_type(ten_loai_san_pham: str, ma_danh_muc: int, slug: str):
    """Tạo mới loại sản phẩm và lưu vào cơ sở dữ liệu.

    Args:
        ten_loai_san_pham (str): Tên loại sản phẩm.
        ma_danh_muc (int): Mã danh mục.
        slug (str): Slug (có thể None).

    Returns:
        ProductType: Loại sản phẩm vừa tạo.
    """
    product_type = ProductType(
        ten_loai_san_pham=ten_loai_san_pham,
        ma_danh_muc=ma_danh_muc,
        slug=slug or None,
    )
    db.session.add(product_type)
    db.session.commit()
    return product_type


def update_product_type(product_type: ProductType, ten_loai_san_pham: str, ma_danh_muc: int, slug: str):
    """Cập nhật thông tin loại sản phẩm và lưu thay đổi.

    Args:
        product_type (ProductType): Loại sản phẩm cần cập nhật.
        ten_loai_san_pham (str): Tên loại sản phẩm mới.
        ma_danh_muc (int): Mã danh mục mới.
        slug (str): Slug mới (có thể None).

    Returns:
        ProductType: Loại sản phẩm sau khi cập nhật.
    """
    product_type.ten_loai_san_pham = ten_loai_san_pham
    product_type.ma_danh_muc = ma_danh_muc
    product_type.slug = slug or None
    db.session.commit()
    return product_type


def soft_delete_product_type(product_type: ProductType):
    """Xoá loại sản phẩm khỏi cơ sở dữ liệu.

    Args:
        product_type (ProductType): Loại sản phẩm cần xoá.
    """
    db.session.delete(product_type)
    db.session.commit()
