"""
Admin Account Management Routes.

This module provides routes for managing user accounts in the admin panel.
"""

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.decorators import admin_required
from app.services.account_service import (
    AccountServiceError,
    DuplicateAccountError,
    ValidationError,
    create_account,
    get_account_or_404,
    get_account_page,
    get_account_stats,
    search_accounts,
    update_account,
)


admin_account_bp = Blueprint(
    "admin_account",
    __name__,
    url_prefix="/admin/accounts",
)


@admin_account_bp.route("/", methods=["GET"])
@admin_required
def show_account_page():
    """Display paginated list of all user accounts.

    Returns:
        Response: Rendered account list template.
    """
    keyword = request.args.get("keyword", "").strip()
    page = request.args.get("page", 1, type=int)

    pagination, accounts, total_accounts = get_account_page(keyword, page)
    stats = get_account_stats()

    return render_template(
        "admin/account/account.html",
        accounts=accounts,
        pagination=pagination,
        total_accounts=total_accounts,
        stats=stats,
        keyword=keyword,
    )


@admin_account_bp.route("/search", methods=["GET"])
@admin_required
def search_account_page():
    """Search accounts by username or email.

    Returns:
        Response: Rendered search results template.
    """
    keyword = request.args.get("keyword", "").strip()
    accounts = search_accounts(keyword)

    return render_template(
        "admin/account/account_search.html",
        accounts=accounts,
        keyword=keyword,
        total_results=len(accounts),
    )


@admin_account_bp.route("/create", methods=["GET", "POST"])
@admin_required
def create_account_page():
    """Handle account creation form display and submission.

    Returns:
        Response: Redirect to account list on success, or render create form.
    """
    errors = {}
    form_data = {}

    if request.method == "POST":
        # Collect form data
        form_data = {
            "ten_tai_khoan": request.form.get("ten_tai_khoan", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", ""),
            "ho_ten": request.form.get("ho_ten", "").strip(),
            "ngay_sinh": request.form.get("ngay_sinh", ""),
            "gioi_tinh": request.form.get("gioi_tinh", "0"),
            "so_dien_thoai": request.form.get("so_dien_thoai", "").strip(),
            "dia_chi": request.form.get("dia_chi", "").strip(),
            "role": request.form.get("role", "0"),
            "trang_thai": request.form.get("trang_thai", "1"),
        }

        # Parse date
        ngay_sinh = None
        if form_data["ngay_sinh"]:
            try:
                ngay_sinh = datetime.strptime(form_data["ngay_sinh"], "%Y-%m-%d")
            except ValueError:
                errors["ngay_sinh"] = "Ngày sinh không hợp lệ."

        if not errors:
            try:
                create_account(
                    ten_tai_khoan=form_data["ten_tai_khoan"],
                    email=form_data["email"],
                    password=form_data["password"],
                    ho_ten=form_data["ho_ten"],
                    ngay_sinh=ngay_sinh,
                    gioi_tinh=int(form_data["gioi_tinh"]),
                    so_dien_thoai=form_data["so_dien_thoai"],
                    dia_chi=form_data["dia_chi"],
                    role=int(form_data["role"]),
                    trang_thai=int(form_data["trang_thai"]),
                )
                flash("Tạo tài khoản thành công!", "success")
                return redirect(url_for("admin_account.show_account_page"))

            except ValidationError as e:
                errors["general"] = str(e)
            except DuplicateAccountError as e:
                errors["general"] = str(e)
            except AccountServiceError as e:
                errors["general"] = f"Lỗi khi tạo tài khoản: {str(e)}"

    return render_template(
        "admin/account/account_create.html",
        errors=errors,
        form_data=form_data,
    )


@admin_account_bp.route("/<int:user_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_account_page(user_id: int):
    """Handle account edit form display and submission.

    Args:
        user_id (int): Account ID to edit.

    Returns:
        Response: Redirect to account list on success, or render edit form.
    """
    account = get_account_or_404(user_id)
    errors = {}

    if request.method == "POST":
        # Collect form data
        ten_tai_khoan = request.form.get("ten_tai_khoan", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        ho_ten = request.form.get("ho_ten", "").strip()
        ngay_sinh_str = request.form.get("ngay_sinh", "")
        gioi_tinh = request.form.get("gioi_tinh", "0")
        so_dien_thoai = request.form.get("so_dien_thoai", "").strip()
        dia_chi = request.form.get("dia_chi", "").strip()
        role = request.form.get("role", "0")
        trang_thai = request.form.get("trang_thai", "1")

        # Parse date
        ngay_sinh = account.ngay_sinh
        if ngay_sinh_str:
            try:
                ngay_sinh = datetime.strptime(ngay_sinh_str, "%Y-%m-%d")
            except ValueError:
                errors["ngay_sinh"] = "Ngày sinh không hợp lệ."

        if not errors:
            try:
                update_account(
                    account=account,
                    ten_tai_khoan=ten_tai_khoan,
                    email=email,
                    ho_ten=ho_ten,
                    ngay_sinh=ngay_sinh,
                    gioi_tinh=int(gioi_tinh),
                    so_dien_thoai=so_dien_thoai,
                    dia_chi=dia_chi,
                    role=int(role),
                    trang_thai=int(trang_thai),
                    password=password if password else None,
                )
                flash("Cập nhật tài khoản thành công!", "success")
                return redirect(url_for("admin_account.show_account_page"))

            except ValidationError as e:
                errors["general"] = str(e)
            except DuplicateAccountError as e:
                errors["general"] = str(e)
            except AccountServiceError as e:
                errors["general"] = f"Lỗi khi cập nhật tài khoản: {str(e)}"

    return render_template(
        "admin/account/account_edit.html",
        account=account,
        errors=errors,
    )
