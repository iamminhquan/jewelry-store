from app.extensions import db
from app.models.category import Category
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_category_query(keyword: str, status: str):
    """Tạo truy vấn danh mục theo từ khoá và trạng thái.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).

    Returns:
        BaseQuery: Truy vấn danh mục đã áp dụng điều kiện lọc.
    """
    query = Category.query

    if status == "1":
        query = query.filter(Category.trang_thai == 1)
    elif status == "2":
        query = query.filter(Category.trang_thai == 2)
    elif status == "3":
        query = query.filter(Category.trang_thai == 3)
    else:
        query = query.filter(Category.trang_thai != 3)

    if keyword:
        query = query.filter(
            or_(
                cast(Category.ma_danh_muc, String).like(f"%{keyword}%"),
                Category.ten_danh_muc.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_category_page(keyword: str, status: str, page: int, per_page: int = 3):
    """Lấy dữ liệu danh mục theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, categories, total_categories, con_hang, het_hang,
        ten_dm_noi_bat)
    """
    query = build_category_query(keyword, status)

    pagination = query.order_by(Category.ma_danh_muc.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_categories = Category.query.filter(Category.trang_thai != 3).count()
    con_hang = Category.query.filter_by(trang_thai=1).count()
    het_hang = Category.query.filter_by(trang_thai=2).count()

    danh_muc_noi_bat = Category.query.filter(Category.trang_thai != 3).limit(3).all()
    ten_dm_noi_bat = ", ".join(dm.ten_danh_muc for dm in danh_muc_noi_bat)

    return (
        pagination,
        pagination.items,
        total_categories,
        con_hang,
        het_hang,
        ten_dm_noi_bat,
    )


def get_category_or_404(category_id: int):
    """Lấy danh mục theo id hoặc trả về 404.

    Args:
        category_id (int): Mã danh mục.

    Returns:
        Category: Danh mục tìm thấy.
    """
    return Category.query.get_or_404(category_id)


def create_category(ten_danh_muc: str, mo_ta: str, trang_thai: int):
    """Tạo mới danh mục và lưu vào cơ sở dữ liệu.

    Args:
        ten_danh_muc (str): Tên danh mục.
        mo_ta (str): Mô tả danh mục.
        trang_thai (int): Trạng thái danh mục.

    Returns:
        Category: Danh mục vừa tạo.
    """
    category = Category(
        ten_danh_muc=ten_danh_muc,
        mo_ta=mo_ta,
        trang_thai=trang_thai,
    )
    db.session.add(category)
    db.session.commit()
    return category


def update_category(category: Category, ten_danh_muc: str, mo_ta: str, new_status: int):
    """Cập nhật thông tin danh mục và lưu thay đổi.

    Args:
        category (Category): Danh mục cần cập nhật.
        ten_danh_muc (str): Tên danh mục mới.
        mo_ta (str): Mô tả mới.
        new_status (int): Trạng thái mới.

    Returns:
        Category: Danh mục sau khi cập nhật.
    """
    category.ten_danh_muc = ten_danh_muc
    category.mo_ta = mo_ta
    category.trang_thai = 3 if new_status == 3 else new_status
    db.session.commit()
    return category


def soft_delete_category(category: Category):
    """Xoá mềm danh mục bằng cách đặt trạng thái đã xoá.

    Args:
        category (Category): Danh mục cần xoá.
    """
    category.trang_thai = 3
    db.session.commit()
