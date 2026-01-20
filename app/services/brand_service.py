from app.extensions import db
from app.models.brand import Brand
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_brand_query(keyword: str):
    """Tạo truy vấn thương hiệu theo từ khoá.

    Args:
        keyword (str): Từ khoá tìm kiếm.

    Returns:
        BaseQuery: Truy vấn thương hiệu đã áp dụng điều kiện lọc.
    """
    query = Brand.query

    if keyword:
        query = query.filter(
            or_(
                cast(Brand.ma_thuong_hieu, String).like(f"%{keyword}%"),
                Brand.ten_thuong_hieu.ilike(f"%{keyword}%"),
                Brand.so_dien_thoai.ilike(f"%{keyword}%"),
                Brand.email.ilike(f"%{keyword}%"),
                Brand.dia_chi.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_brand_page(keyword: str, page: int, per_page: int = 3):
    """Lấy dữ liệu thương hiệu theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, brands, total_brands, ten_th_noi_bat)
    """
    query = build_brand_query(keyword)

    pagination = db.paginate(
        query.order_by(Brand.ma_thuong_hieu.desc()),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_brands = Brand.query.count()

    thuong_hieu_noi_bat = Brand.query.limit(3).all()
    ten_th_noi_bat = ", ".join(th.ten_thuong_hieu for th in thuong_hieu_noi_bat)

    return (
        pagination,
        pagination.items,
        total_brands,
        ten_th_noi_bat,
    )


def get_brand_or_404(brand_id: int):
    """Lấy thương hiệu theo id hoặc trả về 404.

    Args:
        brand_id (int): Mã thương hiệu.

    Returns:
        Brand: Thương hiệu tìm thấy.
    """
    return Brand.query.get_or_404(brand_id)


def create_brand(ten_thuong_hieu: str, so_dien_thoai: str, email: str, dia_chi: str):
    """Tạo mới thương hiệu và lưu vào cơ sở dữ liệu.

    Args:
        ten_thuong_hieu (str): Tên thương hiệu.
        so_dien_thoai (str): Số điện thoại.
        email (str): Email.
        dia_chi (str): Địa chỉ.

    Returns:
        Brand: Thương hiệu vừa tạo.
    """
    brand = Brand(
        ten_thuong_hieu=ten_thuong_hieu,
        so_dien_thoai=so_dien_thoai or None,
        email=email or None,
        dia_chi=dia_chi or None,
    )

    db.session.add(brand)
    db.session.commit()

    return brand


def update_brand(
    brand: Brand,
    ten_thuong_hieu: str,
    so_dien_thoai: str,
    email: str,
    dia_chi: str,
):
    """Cập nhật thông tin thương hiệu và lưu thay đổi.

    Args:
        brand (Brand): Thương hiệu cần cập nhật.
        ten_thuong_hieu (str): Tên thương hiệu mới.
        so_dien_thoai (str): Số điện thoại mới.
        email (str): Email mới.
        dia_chi (str): Địa chỉ mới.

    Returns:
        Brand: Thương hiệu sau khi cập nhật.
    """
    brand.ten_thuong_hieu = ten_thuong_hieu
    brand.so_dien_thoai = so_dien_thoai or None
    brand.email = email or None
    brand.dia_chi = dia_chi or None

    db.session.commit()

    return brand


def soft_delete_brand(brand: Brand):
    """Xoá thương hiệu khỏi cơ sở dữ liệu.

    Args:
        brand (Brand): Thương hiệu cần xoá.
    """
    db.session.delete(brand)
    db.session.commit()
