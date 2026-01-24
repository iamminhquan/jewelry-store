"""
Module service quản lý liên hệ.

Module này cung cấp logic nghiệp vụ cho các thao tác quản lý liên hệ phía admin.
"""

from app.extensions import db
from app.models.contact import Contact
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_contact_query(keyword: str):
    """Tạo truy vấn liên hệ theo từ khoá.

    Args:
        keyword (str): Từ khoá tìm kiếm.

    Returns:
        BaseQuery: Truy vấn liên hệ đã áp dụng điều kiện lọc.
    """
    query = Contact.query

    if keyword:
        query = query.filter(
            or_(
                cast(Contact.ma_lien_he, String).like(f"%{keyword}%"),
                Contact.ten_khach_hang.ilike(f"%{keyword}%"),
                Contact.email.ilike(f"%{keyword}%"),
                Contact.so_dien_thoai.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_contact_page(keyword: str, page: int, per_page: int = 10):
    """Lấy dữ liệu liên hệ theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 10.

    Returns:
        tuple: (pagination, contacts, total_contacts)
    """
    query = build_contact_query(keyword)

    pagination = query.order_by(Contact.ngay_tao.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_contacts = Contact.query.count()

    return (
        pagination,
        pagination.items,
        total_contacts,
    )


def get_contact_or_404(contact_id: int):
    """Lấy liên hệ theo id hoặc trả về 404.

    Args:
        contact_id (int): Mã liên hệ.

    Returns:
        Contact: Liên hệ tìm thấy.
    """
    return Contact.query.get_or_404(contact_id)


def delete_contact(contact: Contact):
    """Xoá liên hệ khỏi cơ sở dữ liệu.

    Args:
        contact (Contact): Liên hệ cần xoá.
    """
    db.session.delete(contact)
    db.session.commit()
