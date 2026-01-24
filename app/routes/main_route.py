from flask import Blueprint, redirect, render_template, session, url_for, request
from flask_login import current_user, login_required, logout_user
from app.extensions import db
from app.services.dashboard_service import get_dashboard_data, get_website_info
from app.models.product import Product
from app.models.order import Order
from app.services.user_product_service import get_best_seller_products, get_new_products
from app.services.favorite_service import get_user_favorites, get_user_favorite_ids
from app.constants import OrderStatus

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/",
)


@main_bp.route("/")
def show_home_page():
    best_sellers = get_best_seller_products()
    new_products = get_new_products()
    slide_products = (
        Product.query.filter(Product.trang_thai == 1)
        .order_by(Product.so_luong.desc())
        .limit(4)
        .all()
    )

    # Lấy danh sách ID sản phẩm yêu thích của user (nếu đã đăng nhập)
    favorite_ids = []
    if current_user.is_authenticated:
        favorite_ids = get_user_favorite_ids(current_user.ma_tai_khoan)

    return render_template(
        "index.html",
        slide_products=slide_products,
        best_sellers=best_sellers,
        new_products=new_products,
        favorite_ids=favorite_ids,
    )


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


@main_bp.route("/shipping")
def show_shipping_page():
    return render_template("pages/shipping.html")


@main_bp.route("/warranty")
def show_warranty_page():
    return render_template("pages/warranty.html")


@main_bp.route("/payment")
def show_payment_page():
    return render_template("pages/payment.html")


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

    # Get user's orders
    orders = Order.query.filter_by(
        ma_tai_khoan=current_user.ma_tai_khoan
    ).order_by(Order.ngay_tao.desc()).all()

    # Get user's favorite products
    favorite_products = get_user_favorites(current_user.ma_tai_khoan)

    return render_template(
        "account.html",
        user=current_user,
        orders=orders,
        OrderStatus=OrderStatus,
        favorite_products=favorite_products,
    )


@main_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("main.show_home_page"))
