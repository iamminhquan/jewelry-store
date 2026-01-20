from app.extensions import db
from app.models.material import Material
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_material_query(keyword: str):
    """Tạo truy vấn chất liệu theo từ khoá.

    Args:
        keyword (str): Từ khoá tìm kiếm.

    Returns:
        BaseQuery: Truy vấn chất liệu đã áp dụng điều kiện lọc.
    """
    query = Material.query

    if keyword:
        query = query.filter(
            or_(
                cast(Material.ma_chat_lieu, String).like(f"%{keyword}%"),
                Material.ten_chat_lieu.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_material_page(keyword: str, page: int, per_page: int = 3):
    """Lấy dữ liệu chất liệu theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, materials, total_materials, ten_cl_noi_bat)
    """
    query = build_material_query(keyword)

    pagination = db.paginate(
        query.order_by(Material.ma_chat_lieu.desc()),
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_materials = Material.query.count()

    chat_lieu_noi_bat = Material.query.limit(3).all()
    ten_cl_noi_bat = ", ".join(cl.ten_chat_lieu for cl in chat_lieu_noi_bat)

    return (
        pagination,
        pagination.items,
        total_materials,
        ten_cl_noi_bat,
    )


def get_material_or_404(material_id: int):
    """Lấy chất liệu theo id hoặc trả về 404.

    Args:
        material_id (int): Mã chất liệu.

    Returns:
        Material: Chất liệu tìm thấy.
    """
    return Material.query.get_or_404(material_id)


def create_material(ten_chat_lieu: str):
    """Tạo mới chất liệu và lưu vào cơ sở dữ liệu.

    Args:
        ten_chat_lieu (str): Tên chất liệu.

    Returns:
        Material: Chất liệu vừa tạo.
    """
    material = Material(
        ten_chat_lieu=ten_chat_lieu,
    )
    db.session.add(material)
    db.session.commit()
    return material


def update_material(material: Material, ten_chat_lieu: str):
    """Cập nhật thông tin chất liệu và lưu thay đổi.

    Args:
        material (Material): Chất liệu cần cập nhật.
        ten_chat_lieu (str): Tên chất liệu mới.

    Returns:
        Material: Chất liệu sau khi cập nhật.
    """
    material.ten_chat_lieu = ten_chat_lieu
    db.session.commit()
    return material


def soft_delete_material(material: Material):
    """Xoá chất liệu khỏi cơ sở dữ liệu.

    Args:
        material (Material): Chất liệu cần xoá.
    """
    db.session.delete(material)
    db.session.commit()
