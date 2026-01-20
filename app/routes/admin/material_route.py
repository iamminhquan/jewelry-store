from flask import Blueprint, render_template, redirect, request, url_for

from app.decorators import admin_required
from app.services.material_service import (
    create_material,
    get_material_or_404,
    get_material_page,
    soft_delete_material,
    update_material,
)


material_bp = Blueprint(
    "material",
    __name__,
    url_prefix="/admin/material",
)


@material_bp.route("/", methods=["GET"])
@admin_required
def show_material_page():
    """Hiển thị trang quản lý chất liệu kèm lọc và phân trang.

    Returns:
        Response: Template danh sách chất liệu đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        materials,
        total_materials,
        ten_cl_noi_bat,
    ) = get_material_page(keyword, page)

    return render_template(
        "admin/material/material.html",
        materials=materials,
        pagination=pagination,
        total_materials=total_materials,
        ten_cl_noi_bat=ten_cl_noi_bat,
    )


@material_bp.route("/create", methods=["GET", "POST"])
@admin_required
def show_create_material_page():
    """Tạo mới chất liệu hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_chat_lieu = request.form.get("ten_chat_lieu", "").strip()

        create_material(ten_chat_lieu)
        return redirect(url_for("material.show_material_page"))

    return render_template("admin/material/material_create.html")


@material_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def show_edit_material_page(id):
    """Cập nhật chất liệu hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã chất liệu cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    material = get_material_or_404(id)

    if request.method == "POST":
        ten_chat_lieu = request.form.get("ten_chat_lieu", "").strip()

        update_material(material, ten_chat_lieu)
        return redirect(url_for("material.show_material_page"))

    return render_template(
        "admin/material/material_edit.html",
        material=material,
    )


@material_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_material(id):
    """Xoá chất liệu khỏi cơ sở dữ liệu.

    Args:
        id (int): Mã chất liệu cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách chất liệu sau khi xoá.
    """
    material = get_material_or_404(id)
    soft_delete_material(material)
    return redirect(url_for("material.show_material_page"))
