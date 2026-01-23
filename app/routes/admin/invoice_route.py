from flask import Blueprint, render_template, redirect, request, url_for, flash

from app.decorators import admin_required
from app.services.invoice_service import (
    create_invoice,
    get_invoice_or_404,
    get_invoice_page,
    soft_delete_invoice,
    update_invoice,
)
from app.services.invoice_detail_service import get_invoice_detail_with_product, create_invoice_detail, delete_invoice_detail
from app.models.account import Account
from app.models.product import Product
from app.models.order import Order


invoice_bp = Blueprint(
    "invoice",
    __name__,
    url_prefix="/admin/invoice",
)


@invoice_bp.route("/", methods=["GET"])
@admin_required
def show_invoice_page():
    """Hiển thị trang quản lý hóa đơn kèm lọc và phân trang.

    Returns:
        Response: Template danh sách hóa đơn đã render.
    """
    keyword = request.args.get("keyword", "").strip()
    status = request.args.get("status")
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()
    min_value = request.args.get("min_value", "").strip()
    max_value = request.args.get("max_value", "").strip()
    page = request.args.get("page", 1, type=int)

    (
        pagination,
        invoices,
        total_invoices,
        cho_xac_nhan,
        dang_xu_ly,
        da_thanh_toan,
        da_huy,
    ) = get_invoice_page(keyword, status, date_from, date_to, min_value, max_value, page)

    # Lấy thông tin khách hàng và đơn hàng cho mỗi hóa đơn
    invoices_with_account = []
    for invoice in invoices:
        account = Account.query.get(invoice.ma_tai_khoan)
        # Safely get order - ma_don_hang might not exist in older database
        order = None
        try:
            if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang:
                order = Order.query.get(invoice.ma_don_hang)
        except Exception:
            pass
        invoices_with_account.append({
            'invoice': invoice,
            'account': account,
            'order': order
        })

    return render_template(
        "admin/invoice/invoice.html",
        invoices_with_account=invoices_with_account,
        pagination=pagination,
        total_invoices=total_invoices,
        cho_xac_nhan=cho_xac_nhan,
        dang_xu_ly=dang_xu_ly,
        da_thanh_toan=da_thanh_toan,
        da_huy=da_huy,
    )


@invoice_bp.route("/create", methods=["GET", "POST"])
@admin_required
def show_create_invoice_page():
    """Tạo mới hóa đơn hoặc hiển thị form tạo.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form tạo.
    """
    if request.method == "POST":
        try:
            ma_tai_khoan = int(request.form.get("ma_tai_khoan"))
            tong_tien_tam_tinh = request.form.get("tong_tien_tam_tinh", "").strip()
            ngay_dat_hang = request.form.get("ngay_dat_hang", "").strip()
            trang_thai = int(request.form.get("trang_thai", 0))
            
            tong_tien = float(tong_tien_tam_tinh) if tong_tien_tam_tinh else None
            
            invoice = create_invoice(ma_tai_khoan, tong_tien, ngay_dat_hang, trang_thai)
            
            # Xử lý chi tiết hóa đơn nếu có
            product_ids = request.form.getlist("product_id[]")
            quantities = request.form.getlist("quantity[]")
            prices = request.form.getlist("price[]")
            
            for i in range(len(product_ids)):
                if product_ids[i] and quantities[i] and prices[i]:
                    try:
                        create_invoice_detail(
                            invoice.ma_hoa_don,
                            int(product_ids[i]),
                            int(quantities[i]),
                            float(prices[i])
                        )
                    except (ValueError, TypeError):
                        continue
            
            flash("Hóa đơn đã được tạo thành công.", "success")
            return redirect(url_for("invoice.show_invoice_page"))
        except (TypeError, ValueError) as e:
            flash("Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.", "error")

    accounts = Account.query.filter(Account.trang_thai == 1).all()  # Chỉ lấy tài khoản đang hoạt động
    products = Product.query.filter(Product.trang_thai == 1).all()  # Chỉ lấy sản phẩm đang bán
    
    return render_template(
        "admin/invoice/invoice_create.html",
        accounts=accounts,
        products=products,
    )


@invoice_bp.route("/detail/<int:id>", methods=["GET"])
@admin_required
def show_invoice_detail_page(id):
    """Hiển thị chi tiết hóa đơn.

    Args:
        id (int): Mã hóa đơn.

    Returns:
        Response: Template chi tiết hóa đơn đã render.
    """
    invoice = get_invoice_or_404(id)
    account = Account.query.get(invoice.ma_tai_khoan)
    
    # Safely get order - ma_don_hang might not exist in older database
    order = None
    try:
        if hasattr(invoice, 'ma_don_hang') and invoice.ma_don_hang:
            order = Order.query.get(invoice.ma_don_hang)
    except Exception:
        pass
    
    invoice_details_with_product = get_invoice_detail_with_product(id)

    return render_template(
        "admin/invoice/invoice_detail.html",
        invoice=invoice,
        account=account,
        order=order,
        invoice_details_with_product=invoice_details_with_product,
    )


@invoice_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def show_edit_invoice_page(id):
    """Điều chỉnh thông tin hóa đơn hoặc hiển thị form chỉnh sửa.

    Args:
        id (int): Mã hóa đơn cần chỉnh sửa.

    Returns:
        Response: Chuyển hướng về danh sách khi thành công, hoặc render form sửa.
    """
    invoice = get_invoice_or_404(id)
    account = Account.query.get(invoice.ma_tai_khoan)

    # Kiểm tra điều kiện chỉnh sửa (không cho sửa nếu đã xóa)
    if invoice.trang_thai == 3:
        flash("Không thể chỉnh sửa hóa đơn đã xóa.", "error")
        return redirect(url_for("invoice.show_invoice_page"))

    if request.method == "POST":
        try:
            ma_tai_khoan = int(request.form.get("ma_tai_khoan"))
            tong_tien_tam_tinh = request.form.get("tong_tien_tam_tinh", "").strip()
            ngay_dat_hang = request.form.get("ngay_dat_hang", "").strip()
            trang_thai = int(request.form.get("trang_thai", invoice.trang_thai))
            
            tong_tien = float(tong_tien_tam_tinh) if tong_tien_tam_tinh else None
            
            update_invoice(invoice, ma_tai_khoan, tong_tien, ngay_dat_hang, trang_thai)
            flash("Thông tin hóa đơn đã được cập nhật thành công.", "success")
            return redirect(url_for("invoice.show_invoice_page"))
        except (TypeError, ValueError) as e:
            flash("Dữ liệu không hợp lệ.", "error")

    accounts = Account.query.filter(Account.trang_thai == 1).all()
    
    return render_template(
        "admin/invoice/invoice_edit.html",
        invoice=invoice,
        account=account,
        accounts=accounts,
    )


@invoice_bp.route("/delete/<int:id>", methods=["POST"])
@admin_required
def delete_invoice(id):
    """Xóa mềm hóa đơn.

    Args:
        id (int): Mã hóa đơn cần xóa.

    Returns:
        Response: Chuyển hướng về danh sách hóa đơn sau khi xóa.
    """
    invoice = get_invoice_or_404(id)
    
    # Kiểm tra điều kiện xóa
    if invoice.trang_thai == 3:
        flash("Hóa đơn này đã được xóa trước đó.", "error")
    else:
        soft_delete_invoice(invoice)
        flash("Hóa đơn đã được xóa thành công.", "success")
    
    return redirect(url_for("invoice.show_invoice_page"))
