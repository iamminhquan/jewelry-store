"""
Module route quản lý liên hệ (Admin).

Blueprint này xử lý các thao tác quản lý liên hệ phía admin bao gồm:
- Xem danh sách liên hệ
- Xem chi tiết liên hệ
- Xoá liên hệ
"""

from flask import Blueprint, render_template, redirect, request, url_for

from app.decorators import admin_required
from app.services.contact_service import (
    get_contact_page,
    get_contact_or_404,
    delete_contact,
)


admin_contact_bp = Blueprint(
    "admin_contact",
    __name__,
    url_prefix="/admin/contact",
)


@admin_contact_bp.route("/", methods=["GET"])
@admin_required
def show_contact_page():
    """Hiển thị trang quản lý liên hệ kèm lọc và phân trang.

    Returns:
        Response: Template danh sách liên hệ đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    pagination, contacts, total_contacts = get_contact_page(keyword, page)

    return render_template(
        "admin/contact/contact.html",
        contacts=contacts,
        pagination=pagination,
        total_contacts=total_contacts,
    )


@admin_contact_bp.route("/detail/<int:id>", methods=["GET"])
@admin_required
def show_contact_detail(id):
    """Hiển thị chi tiết liên hệ.

    Args:
        id (int): Mã liên hệ cần xem.

    Returns:
        Response: Template chi tiết liên hệ.
    """
    contact = get_contact_or_404(id)

    return render_template(
        "admin/contact/contact_detail.html",
        contact=contact,
    )


@admin_contact_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_contact_route(id):
    """Xoá liên hệ.

    Args:
        id (int): Mã liên hệ cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách liên hệ sau khi xoá.
    """
    contact = get_contact_or_404(id)
    delete_contact(contact)
    return redirect(url_for("admin_contact.show_contact_page"))
