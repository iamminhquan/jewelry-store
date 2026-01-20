from flask import Blueprint, render_template, redirect, request, url_for

from app.decorators import admin_required
from app.services.category_service import (
    create_category,
    get_category_or_404,
    get_category_page,
    soft_delete_category,
    update_category,
)


category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="/admin/category",
)


@category_bp.route("/", methods=["GET"])
@admin_required
def show_category_page():
    """Hiển thị trang quản lý danh mục kèm lọc và phân trang.

    Returns:
        Response: Template danh sách danh mục đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        categories,
        total_categories,
        con_hang,
        het_hang,
        ten_dm_noi_bat,
    ) = get_category_page(keyword, status, page)

    return render_template(
        "admin/category/category.html",
        categories=categories,
        pagination=pagination,
        total_categories=total_categories,
        con_hang=con_hang,
        het_hang=het_hang,
        ten_dm_noi_bat=ten_dm_noi_bat,
    )


@category_bp.route("/create", methods=["GET", "POST"])
@admin_required
def show_create_category_page():
    """Tạo mới danh mục hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_danh_muc = request.form.get("ten_danh_muc", "").strip()
        mo_ta = request.form.get("mo_ta")
        try:
            trang_thai = int(request.form.get("trang_thai", 1))
        except (TypeError, ValueError):
            trang_thai = 1

        create_category(ten_danh_muc, mo_ta, trang_thai)
        return redirect(url_for("category.show_category_page"))

    return render_template("admin/category/category_create.html")


@category_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def show_edit_category_page(id):
    """Cập nhật danh mục hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã danh mục cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    category = get_category_or_404(id)

    if request.method == "POST":
        ten_danh_muc = request.form.get("ten_danh_muc", "").strip()
        mo_ta = request.form.get("mo_ta")
        try:
            new_status = int(request.form.get("trang_thai", category.trang_thai))
        except (TypeError, ValueError):
            new_status = category.trang_thai

        update_category(category, ten_danh_muc, mo_ta, new_status)
        return redirect(url_for("category.show_category_page"))

    return render_template(
        "admin/category/category_edit.html",
        category=category,
    )


@category_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_category(id):
    """Xoá mềm danh mục bằng cách chuyển trạng thái sang đã xoá.

    Args:
        id (int): Mã danh mục cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách danh mục sau khi xoá.
    """
    category = get_category_or_404(id)
    soft_delete_category(category)
    return redirect(url_for("category.show_category_page"))
