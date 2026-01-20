from flask import Blueprint, render_template, redirect, request, url_for

from app.decorators import admin_required
from app.services.collection_service import (
    create_collection,
    get_collection_or_404,
    get_collection_page,
    soft_delete_collection,
    update_collection,
)


collection_bp = Blueprint(
    "collection",
    __name__,
    url_prefix="/admin/collection",
)


@collection_bp.route("/", methods=["GET"])
@admin_required
def show_collection_page():
    """Hiển thị trang quản lý bộ sưu tập kèm lọc và phân trang.

    Returns:
        Response: Template danh sách bộ sưu tập đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        collections,
        total_collections,
        con_hang,
        het_hang,
        ten_bst_noi_bat,
    ) = get_collection_page(keyword, status, page)

    return render_template(
        "admin/collection/collection.html",
        collections=collections,
        pagination=pagination,
        total_collections=total_collections,
        con_hang=con_hang,
        het_hang=het_hang,
        ten_bst_noi_bat=ten_bst_noi_bat,
    )


@collection_bp.route("/create", methods=["GET", "POST"])
@admin_required
def show_create_collection_page():
    """Tạo mới bộ sưu tập hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_bo_suu_tap = request.form.get("ten_bo_suu_tap", "").strip()
        mo_ta = request.form.get("mo_ta")
        try:
            trang_thai = int(request.form.get("trang_thai", 1))
        except (TypeError, ValueError):
            trang_thai = 1

        create_collection(ten_bo_suu_tap, mo_ta, trang_thai)
        return redirect(url_for("collection.show_collection_page"))

    return render_template("admin/collection/collection_create.html")


@collection_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def show_edit_collection_page(id):
    """Cập nhật bộ sưu tập hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã bộ sưu tập cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    collection = get_collection_or_404(id)

    if request.method == "POST":
        ten_bo_suu_tap = request.form.get("ten_bo_suu_tap", "").strip()
        mo_ta = request.form.get("mo_ta")
        try:
            new_status = int(request.form.get("trang_thai", collection.trang_thai))
        except (TypeError, ValueError):
            new_status = collection.trang_thai

        update_collection(collection, ten_bo_suu_tap, mo_ta, new_status)
        return redirect(url_for("collection.show_collection_page"))

    return render_template(
        "admin/collection/collection_edit.html",
        collection=collection,
    )


@collection_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_collection(id):
    """Xoá mềm bộ sưu tập bằng cách chuyển trạng thái sang đã xoá.

    Args:
        id (int): Mã bộ sưu tập cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách bộ sưu tập sau khi xoá.
    """
    collection = get_collection_or_404(id)
    soft_delete_collection(collection)
    return redirect(url_for("collection.show_collection_page"))
