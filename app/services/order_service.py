from datetime import datetime
from app.extensions import db
from app.models.order import Order
from app.models.account import Account
from sqlalchemy import or_, cast, func, and_
from sqlalchemy.types import String


def build_order_query(
    keyword: str,
    status: str,
    date_from: str,
    date_to: str,
    min_value: str,
    max_value: str,
):
    """Tạo truy vấn đơn hàng theo từ khoá và các bộ lọc.

    Args:
        keyword (str): Từ khoá tìm kiếm (mã đơn hàng, tên khách hàng).
        status (str): Trạng thái lọc (0, 1, 2, 3, 4, 5 hoặc None).
        date_from (str): Ngày bắt đầu (YYYY-MM-DD).
        date_to (str): Ngày kết thúc (YYYY-MM-DD).
        min_value (str): Giá trị tối thiểu.
        max_value (str): Giá trị tối đa.

    Returns:
        BaseQuery: Truy vấn đơn hàng đã áp dụng điều kiện lọc.
    """
    query = Order.query.outerjoin(Account, Order.ma_tai_khoan == Account.ma_tai_khoan)

    # Lọc theo trạng thái
    if status:
        try:
            status_int = int(status)
            query = query.filter(Order.trang_thai == status_int)
        except (TypeError, ValueError):
            pass

    # Lọc theo ngày
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(func.date(Order.ngay_tao) >= date_from_obj.date())
        except (TypeError, ValueError):
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(func.date(Order.ngay_tao) <= date_to_obj.date())
        except (TypeError, ValueError):
            pass

    # Lọc theo giá trị
    if min_value:
        try:
            min_value_float = float(min_value)
            query = query.filter(Order.tong_tien_tam_tinh >= min_value_float)
        except (TypeError, ValueError):
            pass

    if max_value:
        try:
            max_value_float = float(max_value)
            query = query.filter(Order.tong_tien_tam_tinh <= max_value_float)
        except (TypeError, ValueError):
            pass

    # Tìm kiếm theo keyword
    if keyword:
        query = query.filter(
            or_(
                cast(Order.ma_don_hang, String).like(f"%{keyword}%"),
                Account.ho_ten.ilike(f"%{keyword}%"),
                Account.ten_tai_khoan.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_order_page(
    keyword: str,
    status: str,
    date_from: str,
    date_to: str,
    min_value: str,
    max_value: str,
    page: int,
    per_page: int = 10,
):
    """Lấy dữ liệu đơn hàng theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc.
        date_from (str): Ngày bắt đầu.
        date_to (str): Ngày kết thúc.
        min_value (str): Giá trị tối thiểu.
        max_value (str): Giá trị tối đa.
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 10.

    Returns:
        tuple: (pagination, orders, total_orders, cho_xac_nhan, dang_xu_ly, dang_giao, da_giao, da_huy)
    """
    query = build_order_query(keyword, status, date_from, date_to, min_value, max_value)

    pagination = query.order_by(Order.ma_don_hang.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    # Thống kê theo trạng thái
    total_orders = Order.query.count()
    cho_xac_nhan = Order.query.filter_by(trang_thai=0).count()
    dang_xu_ly = Order.query.filter_by(trang_thai=1).count()
    dang_giao = Order.query.filter_by(trang_thai=2).count()
    da_giao = Order.query.filter_by(trang_thai=3).count()
    da_huy = Order.query.filter_by(trang_thai=4).count()

    return (
        pagination,
        pagination.items,
        total_orders,
        cho_xac_nhan,
        dang_xu_ly,
        dang_giao,
        da_giao,
        da_huy,
    )


def get_order_or_404(order_id: int):
    """Lấy đơn hàng theo id hoặc trả về 404.

    Args:
        order_id (int): Mã đơn hàng.

    Returns:
        Order: Đơn hàng tìm thấy.
    """
    return Order.query.get_or_404(order_id)


def update_order_status(order: Order, new_status: int):
    """Cập nhật trạng thái đơn hàng.

    Args:
        order (Order): Đơn hàng cần cập nhật.
        new_status (int): Trạng thái mới.

    Returns:
        Order: Đơn hàng sau khi cập nhật.
    """
    order.trang_thai = new_status
    if new_status == 1:  # Đang xử lý
        order.ngay_dat_hang = datetime.utcnow()
    db.session.commit()
    return order


def confirm_order(order: Order):
    """Xác nhận đơn hàng (chuyển sang trạng thái đang xử lý).

    Args:
        order (Order): Đơn hàng cần xác nhận.

    Returns:
        Order: Đơn hàng sau khi xác nhận.
    """
    if order.trang_thai == 0:  # Chỉ xác nhận nếu đang chờ xác nhận
        order.trang_thai = 1
        order.ngay_dat_hang = datetime.utcnow()
        db.session.commit()
    return order


def cancel_order(order: Order):
    """Hủy đơn hàng (chuyển sang trạng thái đã hủy).

    Args:
        order (Order): Đơn hàng cần hủy.

    Returns:
        Order: Đơn hàng sau khi hủy.
    """
    # Chỉ cho phép hủy nếu đơn hàng chưa được giao hoặc đã hoàn thành
    if order.trang_thai in [0, 1, 2]:  # Chờ xác nhận, Đang xử lý, Đang giao
        order.trang_thai = 4  # Đã hủy
        db.session.commit()
    return order


def update_order(
    order: Order, tong_tien_tam_tinh: float = None, ngay_dat_hang: str = None
):
    """Điều chỉnh thông tin đơn hàng.

    Args:
        order (Order): Đơn hàng cần cập nhật.
        tong_tien_tam_tinh (float, optional): Tổng tiền tạm tính mới.
        ngay_dat_hang (str, optional): Ngày đặt hàng mới (YYYY-MM-DD).

    Returns:
        Order: Đơn hàng sau khi cập nhật.
    """
    # Chỉ cho phép điều chỉnh nếu đơn hàng chưa được giao
    if order.trang_thai not in [3, 4]:  # Chưa giao hoặc hủy
        if tong_tien_tam_tinh is not None:
            order.tong_tien_tam_tinh = tong_tien_tam_tinh

        if ngay_dat_hang:
            try:
                order.ngay_dat_hang = datetime.strptime(ngay_dat_hang, "%Y-%m-%d")
            except (TypeError, ValueError):
                pass

        db.session.commit()
    return order
