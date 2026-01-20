from datetime import date, datetime, timedelta
from typing import Tuple

from sqlalchemy import func

from app.extensions import db
from app.models.invoice import Invoice
from app.models.order import Order


def _month_boundaries(today: date) -> Tuple[datetime, datetime, datetime, datetime]:
    """Tính mốc thời gian đầu/cuối tháng hiện tại và tháng trước."""
    start_current = date(today.year, today.month, 1)
    start_last = (start_current - timedelta(days=1)).replace(day=1)
    end_last = datetime.combine(start_current, datetime.min.time()) - timedelta(seconds=1)
    return (
        datetime.combine(start_current, datetime.min.time()),
        datetime.combine(today, datetime.max.time()),
        datetime.combine(start_last, datetime.min.time()),
        end_last,
    )


def _safe_percent_change(current: float, previous: float) -> float:
    """Tính % thay đổi, trả về 0 nếu không có dữ liệu so sánh."""
    if previous in (0, None):
        return 0.0
    return round(((current - previous) / previous) * 100, 2)


def get_revenue_stats(days: int = 30):
    """Tính toán các chỉ số doanh thu."""
    today = date.today()
    start_current, end_current, start_last, end_last = _month_boundaries(today)
    days_ago = datetime.combine(today - timedelta(days=days - 1), datetime.min.time())

    base_query = Invoice.query.filter(Invoice.trang_thai != 3)

    total_revenue = (
        db.session.query(func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0))
        .filter(Invoice.trang_thai != 3)
        .scalar()
        or 0
    )

    revenue_this_month = (
        db.session.query(func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0))
        .filter(Invoice.trang_thai != 3, Invoice.ngay_tao >= start_current, Invoice.ngay_tao <= end_current)
        .scalar()
        or 0
    )

    revenue_last_month = (
        db.session.query(func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0))
        .filter(Invoice.trang_thai != 3, Invoice.ngay_tao >= start_last, Invoice.ngay_tao <= end_last)
        .scalar()
        or 0
    )

    daily_revenue_rows = (
        base_query.filter(Invoice.ngay_tao >= days_ago)
        .with_entities(func.date(Invoice.ngay_tao).label("day"), func.coalesce(func.sum(Invoice.tong_tien_tam_tinh), 0).label("amount"))
        .group_by(func.date(Invoice.ngay_tao))
        .order_by(func.date(Invoice.ngay_tao))
        .all()
    )

    daily_revenue = [
        {"date": row.day.strftime("%d/%m"), "amount": float(row.amount or 0)}
        for row in daily_revenue_rows
    ]

    return {
        "total_revenue": float(total_revenue),
        "revenue_this_month": float(revenue_this_month),
        "revenue_last_month": float(revenue_last_month),
        "growth_percent": _safe_percent_change(revenue_this_month, revenue_last_month),
        "daily_revenue": daily_revenue,
    }


def get_purchase_stats(days: int = 30):
    """Tính toán các chỉ số lượt mua (đơn hàng)."""
    today = date.today()
    start_current, end_current, start_last, end_last = _month_boundaries(today)
    days_ago = datetime.combine(today - timedelta(days=days - 1), datetime.min.time())

    total_orders = Order.query.count()
    delivered = Order.query.filter_by(trang_thai=3).count()
    cancelled = Order.query.filter_by(trang_thai=4).count()
    pending = Order.query.filter(Order.trang_thai.in_([0, 1, 2])).count()

    orders_this_month = (
        Order.query.filter(Order.ngay_tao >= start_current, Order.ngay_tao <= end_current).count()
    )
    orders_last_month = (
        Order.query.filter(Order.ngay_tao >= start_last, Order.ngay_tao <= end_last).count()
    )

    daily_orders_rows = (
        Order.query.filter(Order.ngay_tao >= days_ago)
        .with_entities(func.date(Order.ngay_tao).label("day"), func.count(Order.ma_don_hang).label("total"))
        .group_by(func.date(Order.ngay_tao))
        .order_by(func.date(Order.ngay_tao))
        .all()
    )

    daily_orders = [
        {"date": row.day.strftime("%d/%m"), "total": int(row.total or 0)}
        for row in daily_orders_rows
    ]

    cancel_rate = round((cancelled / total_orders) * 100, 2) if total_orders else 0.0

    return {
        "total_orders": total_orders,
        "delivered": delivered,
        "cancelled": cancelled,
        "pending": pending,
        "orders_this_month": orders_this_month,
        "orders_last_month": orders_last_month,
        "growth_percent": _safe_percent_change(orders_this_month, orders_last_month),
        "daily_orders": daily_orders,
        "cancel_rate": cancel_rate,
    }


def build_report_data():
    """Tổng hợp dữ liệu cho trang báo cáo."""
    revenue_stats = get_revenue_stats()
    purchase_stats = get_purchase_stats()

    avg_order_value = 0.0
    if purchase_stats["total_orders"]:
        avg_order_value = round(revenue_stats["total_revenue"] / purchase_stats["total_orders"], 2)

    return {
        "revenue_stats": revenue_stats,
        "purchase_stats": {**purchase_stats, "avg_order_value": avg_order_value},
        "status_breakdown": [
            {
                "label": "Đã giao",
                "value": purchase_stats["delivered"],
                "percent": round((purchase_stats["delivered"] / purchase_stats["total_orders"]) * 100, 1)
                if purchase_stats["total_orders"]
                else 0.0,
                "color": "bg-emerald-500",
            },
            {
                "label": "Đang xử lý",
                "value": purchase_stats["pending"],
                "percent": round((purchase_stats["pending"] / purchase_stats["total_orders"]) * 100, 1)
                if purchase_stats["total_orders"]
                else 0.0,
                "color": "bg-amber-400",
            },
            {
                "label": "Đã hủy",
                "value": purchase_stats["cancelled"],
                "percent": purchase_stats["cancel_rate"],
                "color": "bg-rose-500",
            },
        ],
    }
