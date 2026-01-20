from flask import Blueprint, render_template, redirect, request, url_for

from app.services.brand_service import (
    create_brand,
    get_brand_or_404,
    get_brand_page,
    soft_delete_brand,
    update_brand,
)


brand_bp = Blueprint(
    "brand",
    __name__,
    url_prefix="/admin/brand",
)


@brand_bp.route("/", methods=["GET"])
def show_brand_page():
    """Hiển thị trang quản lý thương hiệu kèm lọc và phân trang.

    Returns:
        Response: Template danh sách thương hiệu đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        brands,
        total_brands,
        ten_th_noi_bat,
    ) = get_brand_page(keyword, page)

    return render_template(
        "admin/brand/brand.html",
        brands=brands,
        pagination=pagination,
        total_brands=total_brands,
        ten_th_noi_bat=ten_th_noi_bat,
    )


@brand_bp.route("/create", methods=["GET", "POST"])
def show_create_brand_page():
    """Tạo mới thương hiệu hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_thuong_hieu = request.form.get("ten_thuong_hieu", "").strip()
        so_dien_thoai = request.form.get("so_dien_thoai", "").strip()
        email = request.form.get("email", "").strip()
        dia_chi = request.form.get("dia_chi", "").strip()

        create_brand(ten_thuong_hieu, so_dien_thoai, email, dia_chi)
        return redirect(url_for("brand.show_brand_page"))

    return render_template("admin/brand/brand_create.html")


@brand_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def show_edit_brand_page(id):
    """Cập nhật thương hiệu hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã thương hiệu cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    brand = get_brand_or_404(id)

    if request.method == "POST":
        ten_thuong_hieu = request.form.get("ten_thuong_hieu", "").strip()
        so_dien_thoai = request.form.get("so_dien_thoai", "").strip()
        email = request.form.get("email", "").strip()
        dia_chi = request.form.get("dia_chi", "").strip()

        update_brand(brand, ten_thuong_hieu, so_dien_thoai, email, dia_chi)
        return redirect(url_for("brand.show_brand_page"))

    return render_template(
        "admin/brand/brand_edit.html",
        brand=brand,
    )


@brand_bp.route("/delete/<int:id>", methods=["POST"])
def delete_brand(id):
    """Xoá thương hiệu khỏi cơ sở dữ liệu.

    Args:
        id (int): Mã thương hiệu cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách thương hiệu sau khi xoá.
    """
    brand = get_brand_or_404(id)
    soft_delete_brand(brand)
    return redirect(url_for("brand.show_brand_page"))
