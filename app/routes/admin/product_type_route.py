from flask import Blueprint, render_template, redirect, request, url_for

from app.decorators import admin_required
from app.services.product_type_service import (
    create_product_type,
    get_all_categories,
    get_product_type_or_404,
    get_product_type_page,
    soft_delete_product_type,
    update_product_type,
)


product_type_bp = Blueprint(
    "product_type",
    __name__,
    url_prefix="/admin/product_type",
)


@product_type_bp.route("/", methods=["GET"])
@admin_required
def show_product_type_page():
    """Hiển thị trang quản lý loại sản phẩm kèm lọc và phân trang.

    Returns:
        Response: Template danh sách loại sản phẩm đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    ma_danh_muc = request.args.get("ma_danh_muc")
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        product_types,
        total_product_types,
        ten_lsp_noi_bat,
    ) = get_product_type_page(keyword, ma_danh_muc, page)

    categories = get_all_categories()

    return render_template(
        "admin/product_type/product_type.html",
        product_types=product_types,
        pagination=pagination,
        total_product_types=total_product_types,
        ten_lsp_noi_bat=ten_lsp_noi_bat,
        categories=categories,
    )


@product_type_bp.route("/create", methods=["GET", "POST"])
@admin_required
def show_create_product_type_page():
    """Tạo mới loại sản phẩm hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_loai_san_pham = request.form.get("ten_loai_san_pham", "").strip()
        slug = request.form.get("slug", "").strip()
        try:
            ma_danh_muc = int(request.form.get("ma_danh_muc"))
        except (TypeError, ValueError):
            return redirect(url_for("product_type.show_create_product_type_page"))

        create_product_type(ten_loai_san_pham, ma_danh_muc, slug)
        return redirect(url_for("product_type.show_product_type_page"))

    categories = get_all_categories()
    return render_template(
        "admin/product_type/product_type_create.html",
        categories=categories,
    )


@product_type_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def show_edit_product_type_page(id):
    """Cập nhật loại sản phẩm hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã loại sản phẩm cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    product_type = get_product_type_or_404(id)

    if request.method == "POST":
        ten_loai_san_pham = request.form.get("ten_loai_san_pham", "").strip()
        slug = request.form.get("slug", "").strip()
        try:
            ma_danh_muc = int(request.form.get("ma_danh_muc"))
        except (TypeError, ValueError):
            ma_danh_muc = product_type.ma_danh_muc

        update_product_type(product_type, ten_loai_san_pham, ma_danh_muc, slug)
        return redirect(url_for("product_type.show_product_type_page"))

    categories = get_all_categories()
    return render_template(
        "admin/product_type/product_type_edit.html",
        product_type=product_type,
        categories=categories,
    )


@product_type_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_product_type(id):
    """Xoá loại sản phẩm khỏi cơ sở dữ liệu.

    Args:
        id (int): Mã loại sản phẩm cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách loại sản phẩm sau khi xoá.
    """
    product_type = get_product_type_or_404(id)
    soft_delete_product_type(product_type)
    return redirect(url_for("product_type.show_product_type_page"))
