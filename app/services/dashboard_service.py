from datetime import datetime, timedelta, date
from typing import Dict, Any

from sqlalchemy import func, and_

from app.extensions import db
from app.models.product import Product
from app.models.order import Order
from app.models.invoice import Invoice
from app.models.account import Account
from app.models.category import Category
from app.models.brand import Brand


def get_today_revenue() -> Dict[str, Any]:
    """Tính doanh thu hôm nay và so sánh với hôm qua."""
    today = date.today()
    yesterday = today - timedelta(days=1)

    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    yesterday_start = datetime.combine(yesterday, datetime.min.time())
    yesterday_end = datetime.combine(yesterday, datetime.max.time())

    # Doanh thu hôm nay từ hóa đơn
    today_revenue = (
        db.session.query(func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0))
        .filter(
            Invoice.trang_thai != 3,  # Không tính hóa đơn đã xóa
            Invoice.ngay_tao >= today_start,
            Invoice.ngay_tao <= today_end
        )
        .scalar() or 0
    )

    # Doanh thu hôm qua
    yesterday_revenue = (
        db.session.query(func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0))
        .filter(
            Invoice.trang_thai != 3,
            Invoice.ngay_tao >= yesterday_start,
            Invoice.ngay_tao <= yesterday_end
        )
        .scalar() or 0
    )

    growth = yesterday_revenue - today_revenue if yesterday_revenue > 0 else today_revenue

    return {
        "amount": float(today_revenue),
        "growth": float(growth),
        "formatted_amount": f"₫{today_revenue:,.0f}",
        "formatted_growth": f"₫{abs(growth):,.0f}",
        "is_increase": growth >= 0
    }


def get_order_stats() -> Dict[str, Any]:
    """Thống kê đơn hàng."""
    total_orders = Order.query.count()
    pending_orders = Order.query.filter(Order.trang_thai.in_([0, 1, 2])).count()  # Chờ xác nhận, đang xử lý, đang giao
    completed_orders = Order.query.filter_by(trang_thai=3).count()
    cancelled_orders = Order.query.filter_by(trang_thai=4).count()

    # Đơn hàng mới hôm nay
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    new_orders_today = (
        Order.query.filter(
            Order.ngay_tao >= today_start,
            Order.ngay_tao <= today_end
        ).count()
    )

    return {
        "total": total_orders,
        "new_today": new_orders_today,
        "pending": pending_orders,
        "completed": completed_orders,
        "cancelled": cancelled_orders
    }


def get_customer_stats() -> Dict[str, Any]:
    """Thống kê khách hàng."""
    total_customers = Account.query.filter_by(role=0).count()  # role=0 là khách hàng
    active_customers = Account.query.filter_by(role=0, trang_thai=1).count()

    # Khách hàng mới hôm nay
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    new_customers_today = (
        Account.query.filter(
            Account.role == 0,  # Khách hàng
            Account.ngay_sinh >= today_start,  # Sử dụng ngay_sinh làm ngày tạo (có thể cần điều chỉnh)
        ).count()
    )

    return {
        "total": total_customers,
        "active": active_customers,
        "new_today": new_customers_today
    }


def get_product_stats() -> Dict[str, Any]:
    """Thống kê sản phẩm."""
    total_products = Product.query.count()
    active_products = Product.query.filter_by(trang_thai=1).count()

    # Sản phẩm hết hàng (so_luong = 0)
    out_of_stock = Product.query.filter_by(so_luong=0).count()

    # Sản phẩm sắp hết hàng (so_luong <= 10)
    low_stock = Product.query.filter(
        Product.trang_thai == 1,
        Product.so_luong > 0,
        Product.so_luong <= 10
    ).count()

    return {
        "total": total_products,
        "active": active_products,
        "out_of_stock": out_of_stock,
        "low_stock": low_stock
    }


def get_category_stats() -> Dict[str, Any]:
    """Thống kê danh mục."""
    total_categories = Category.query.count()
    active_categories = Category.query.filter_by(trang_thai=1).count()

    return {
        "total": total_categories,
        "active": active_categories
    }


def get_brand_stats() -> Dict[str, Any]:
    """Thống kê thương hiệu."""
    total_brands = Brand.query.count()

    return {
        "total": total_brands
    }


def get_recent_orders(limit: int = 5) -> list:
    """Lấy danh sách đơn hàng gần đây."""
    orders = (
        Order.query
        .outerjoin(Account, Order.ma_tai_khoan == Account.ma_tai_khoan)
        .order_by(Order.ngay_tao.desc())
        .limit(limit)
        .all()
    )

    result = []
    for order in orders:
        status_info = get_order_status_info(order.trang_thai)
        result.append({
            "id": order.ma_don_hang,
            "customer_name": getattr(order, 'account', None).ho_ten if getattr(order, 'account', None) else "N/A",
            "total": float(order.tong_tien_tam_tinh or 0),
            "formatted_total": f"₫{order.tong_tien_tam_tinh or 0:,.0f}",
            "status": status_info["label"],
            "status_class": status_info["class"],
            "created_at": order.ngay_tao.strftime("%d/%m/%Y %H:%M") if order.ngay_tao else ""
        })

    return result


def get_low_stock_products(limit: int = 5) -> list:
    """Lấy danh sách sản phẩm sắp hết hàng."""
    products = (
        Product.query
        .filter(
            Product.trang_thai == 1,
            Product.so_luong <= 10,
            Product.so_luong > 0
        )
        .order_by(Product.so_luong.asc())
        .limit(limit)
        .all()
    )

    result = []
    for product in products:
        result.append({
            "id": product.ma_san_pham,
            "name": product.ten_san_pham,
            "stock": product.so_luong,
            "status": "warning" if product.so_luong <= 5 else "normal"
        })

    return result


def get_out_of_stock_products(limit: int = 5) -> list:
    """Lấy danh sách sản phẩm hết hàng."""
    products = (
        Product.query
        .filter(
            Product.trang_thai == 1,
            Product.so_luong == 0
        )
        .order_by(Product.ten_san_pham)
        .limit(limit)
        .all()
    )

    result = []
    for product in products:
        result.append({
            "id": product.ma_san_pham,
            "name": product.ten_san_pham,
            "stock": 0,
            "status": "danger"
        })

    return result


def get_order_status_info(status: int) -> Dict[str, str]:
    """Lấy thông tin trạng thái đơn hàng."""
    status_map = {
        0: {"label": "Chờ xác nhận", "class": "bg-amber-50 text-amber-600"},
        1: {"label": "Đang xử lý", "class": "bg-blue-50 text-blue-600"},
        2: {"label": "Đang giao", "class": "bg-purple-50 text-purple-600"},
        3: {"label": "Đã giao", "class": "bg-emerald-50 text-emerald-600"},
        4: {"label": "Đã hủy", "class": "bg-rose-50 text-rose-600"},
    }
    return status_map.get(status, {"label": "Không xác định", "class": "bg-slate-50 text-slate-600"})


def get_dashboard_data() -> Dict[str, Any]:
    """Tổng hợp tất cả dữ liệu cho dashboard."""
    return {
        "revenue": get_today_revenue(),
        "orders": get_order_stats(),
        "customers": get_customer_stats(),
        "products": get_product_stats(),
        "categories": get_category_stats(),
        "brands": get_brand_stats(),
        "recent_orders": get_recent_orders(),
        "low_stock_products": get_low_stock_products(),
        "out_of_stock_products": get_out_of_stock_products(),
    }


def get_website_info() -> Dict[str, str]:

    return {
        "name": "Jewelry Store",
        "description": "Cửa hàng trang sức cao cấp với các sản phẩm chất lượng",
        "phone": "0123 456 789",
        "email": "contact@jewelry-store.com",
        "address": "65 Đường Huỳnh Thúc Kháng, Quận 1, TP.HCM",
        "working_hours": "8:00 - 18:00 (Thứ 2 - Chủ nhật)"
    }