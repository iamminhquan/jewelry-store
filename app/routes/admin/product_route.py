from flask import Blueprint, render_template, redirect, request, url_for

from app.models import Product
from app.services.product_service import (
    create_product,
    get_product_or_404,
    get_product_page,
    soft_delete_product,
    update_product,
)

from app.services.product_service import get_all_products

product_bp = Blueprint(
    "product",
    __name__,
    url_prefix="/admin/product",
)


@product_bp.route("/", methods=["GET"])
def show_all_products():
    """Hiển thị trang quản lý sản phẩm kèm lọc và phân trang.

    Returns:
        Response: Template danh sách sản phẩm đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        products,
        total_products,
        con_hang,
        het_hang,
        ten_sp_noi_bat,
    ) = get_product_page(keyword, status, page)

    return render_template(
        "admin/product/product.html",
        products=products,
        pagination=pagination,
        total_products=total_products,
        con_hang=con_hang,
        het_hang=het_hang,
        ten_sp_noi_bat=ten_sp_noi_bat,
    )


@product_bp.route("/create", methods=["GET", "POST"])
def show_create_product_page():
    """Tạo mới sản phẩm hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        ten_san_pham = request.form.get("ten_san_pham", "").strip()
        mo_ta = request.form.get("mo_ta")
        don_vi_tinh = request.form.get("don_vi_tinh", "").strip()

        try:
            gia_nhap = float(request.form.get("gia_nhap", 0))
        except (TypeError, ValueError):
            gia_nhap = 0
        try:
            gia_xuat = float(request.form.get("gia_xuat", 0))
        except (TypeError, ValueError):
            gia_xuat = 0
        try:
            trong_luong = float(request.form.get("trong_luong", 0))
        except (TypeError, ValueError):
            trong_luong = 0
        try:
            ma_kich_thuoc = float(request.form.get("ma_kich_thuoc", 0))
        except (TypeError, ValueError):
            ma_kich_thuoc = 0
        try:
            gioi_tinh = int(request.form.get("gioi_tinh", 0))
        except (TypeError, ValueError):
            gioi_tinh = 0
        try:
            so_luong = int(request.form.get("so_luong", 0))
        except (TypeError, ValueError):
            so_luong = 0
        try:
            trang_thai = int(request.form.get("trang_thai", 1))
        except (TypeError, ValueError):
            trang_thai = 1

        create_product(
            ten_san_pham,
            gia_nhap,
            gia_xuat,
            trong_luong,
            ma_kich_thuoc,
            gioi_tinh,
            so_luong,
            don_vi_tinh,
            trang_thai,
            mo_ta,
        )
        return redirect(url_for("product.show_all_products"))

    return render_template("admin/product/product_create.html")


@product_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def show_edit_product_page(id):
    """Cập nhật sản phẩm hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã sản phẩm cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    product = get_product_or_404(id)

    if request.method == "POST":
        ten_san_pham = request.form.get("ten_san_pham", "").strip()
        mo_ta = request.form.get("mo_ta")
        don_vi_tinh = request.form.get("don_vi_tinh", "").strip()

        try:
            gia_nhap = float(request.form.get("gia_nhap", product.gia_nhap))
        except (TypeError, ValueError):
            gia_nhap = product.gia_nhap
        try:
            gia_xuat = float(request.form.get("gia_xuat", product.gia_xuat))
        except (TypeError, ValueError):
            gia_xuat = product.gia_xuat
        try:
            trong_luong = float(request.form.get("trong_luong", product.trong_luong))
        except (TypeError, ValueError):
            trong_luong = product.trong_luong
        try:
            ma_kich_thuoc = float(
                request.form.get("ma_kich_thuoc", product.ma_kich_thuoc)
            )
        except (TypeError, ValueError):
            ma_kich_thuoc = product.ma_kich_thuoc
        try:
            gioi_tinh = int(request.form.get("gioi_tinh", product.gioi_tinh))
        except (TypeError, ValueError):
            gioi_tinh = product.gioi_tinh
        try:
            so_luong = int(request.form.get("so_luong", product.so_luong))
        except (TypeError, ValueError):
            so_luong = product.so_luong
        try:
            new_status = int(request.form.get("trang_thai", product.trang_thai))
        except (TypeError, ValueError):
            new_status = product.trang_thai

        update_product(
            product,
            ten_san_pham,
            gia_nhap,
            gia_xuat,
            trong_luong,
            ma_kich_thuoc,
            gioi_tinh,
            so_luong,
            don_vi_tinh,
            new_status,
            mo_ta,
        )
        return redirect(url_for("product.show_all_products"))

    return render_template(
        "admin/product/product_edit.html",
        product=product,
    )


@product_bp.route("/delete/<int:id>", methods=["POST"])
def delete_product(id):
    """Xoá mềm sản phẩm bằng cách chuyển trạng thái sang đã xoá.

    Args:
        id (int): Mã sản phẩm cần xoá.

    Returns:
        Response: Chuyển hướng về danh sách sản phẩm sau khi xoá.
    """
    product = get_product_or_404(id)
    soft_delete_product(product)
    return redirect(url_for("product.show_all_products"))
