from flask import Blueprint, redirect, render_template, session, url_for, request
from flask_login import current_user, login_required, logout_user
from app.extensions import db
from app.services.dashboard_service import get_dashboard_data, get_website_info


main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/",
)


@main_bp.route("/")
def show_home_page():
    return render_template("index.html")


@main_bp.route("/admin")
@login_required
def show_admin_dashboard():
    # Kiểm tra quyền admin (role=1 là admin, role=0 là khách hàng)
    if current_user.role != 1:
        return redirect(url_for("auth.show_sign_in_page"))
    
    dashboard_data = get_dashboard_data()
    website_info = get_website_info()
    return render_template(
        "admin/index.html",
        revenue=dashboard_data["revenue"],
        orders=dashboard_data["orders"],
        customers=dashboard_data["customers"],
        products=dashboard_data["products"],
        categories=dashboard_data["categories"],
        brands=dashboard_data["brands"],
        recent_orders=dashboard_data["recent_orders"],
        low_stock_products=dashboard_data["low_stock_products"],
        out_of_stock_products=dashboard_data["out_of_stock_products"],
        website_info=website_info,
    )


@main_bp.route("/about")
def show_about_page():
    return render_template("about.html")


@main_bp.route("/login")
def show_login_page():
    return redirect(url_for("auth.show_sign_in_page"))


@main_bp.route("/register")
def show_register_page():
    return redirect(url_for("auth.show_sign_up_page"))


@main_bp.route("/account", methods=["GET", "POST"])
@login_required
def show_account_page():
    if request.method == "POST":
        user = current_user
        user.ho_ten = request.form.get("ho_ten")
        user.email = request.form.get("email")
        user.so_dien_thoai = request.form.get("so_dien_thoai")
        user.dia_chi = request.form.get("dia_chi")
        user.gioi_tinh = request.form.get("gioi_tinh")
        user.ngay_sinh = request.form.get("ngay_sinh") or None

        db.session.commit()

    return render_template(
        "account.html",
        user=current_user,
    )


@main_bp.route("/cart", methods=["GET"])
@login_required
def show_cart_page():
    cart_items = session.get("cart", [])

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    pagination = {"page": 1, "total_pages": 1}

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total_price=total_price,
        pagination=pagination,
        user=current_user,
    )


@main_bp.route("/checkouts", methods=["GET", "POST"])
@login_required
def show_checkouts_page():
    """Trang thanh toán"""
    return render_template("/checkouts.html")


@main_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("main.show_home_page"))
