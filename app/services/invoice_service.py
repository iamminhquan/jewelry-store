from datetime import datetime
from app.extensions import db
from app.models.invoice import Invoice
from app.models.account import Account
from sqlalchemy import or_, cast, func
from sqlalchemy.types import String


def build_invoice_query(keyword: str, status: str, date_from: str, date_to: str, min_value: str, max_value: str):
    """Tạo truy vấn hóa đơn theo từ khoá và các bộ lọc.

    Args:
        keyword (str): Từ khoá tìm kiếm (mã hóa đơn, tên khách hàng).
        status (str): Trạng thái lọc (0, 1, 2, 3 hoặc None).
        date_from (str): Ngày bắt đầu (YYYY-MM-DD).
        date_to (str): Ngày kết thúc (YYYY-MM-DD).
        min_value (str): Giá trị tối thiểu.
        max_value (str): Giá trị tối đa.

    Returns:
        BaseQuery: Truy vấn hóa đơn đã áp dụng điều kiện lọc.
    """
    query = Invoice.query.outerjoin(Account, Invoice.ma_tai_khoan == Account.ma_tai_khoan)

    # Lọc theo trạng thái (loại trừ đã xóa - trạng thái 3)
    if status:
        try:
            status_int = int(status)
            query = query.filter(Invoice.trang_thai == status_int)
        except (TypeError, ValueError):
            pass
    else:
        # Mặc định loại trừ các hóa đơn đã xóa
        query = query.filter(Invoice.trang_thai != 3)

    # Lọc theo ngày
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(func.date(Invoice.ngay_tao) >= date_from_obj.date())
        except (TypeError, ValueError):
            pass

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(func.date(Invoice.ngay_tao) <= date_to_obj.date())
        except (TypeError, ValueError):
            pass

    # Lọc theo giá trị
    if min_value:
        try:
            min_value_float = float(min_value)
            query = query.filter(Invoice.tong_tien_tam_tinh >= min_value_float)
        except (TypeError, ValueError):
            pass

    if max_value:
        try:
            max_value_float = float(max_value)
            query = query.filter(Invoice.tong_tien_tam_tinh <= max_value_float)
        except (TypeError, ValueError):
            pass

    # Tìm kiếm theo keyword
    if keyword:
        query = query.filter(
            or_(
                cast(Invoice.ma_hoa_don, String).like(f"%{keyword}%"),
                Account.ho_ten.ilike(f"%{keyword}%"),
                Account.ten_tai_khoan.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_invoice_page(keyword: str, status: str, date_from: str, date_to: str, min_value: str, max_value: str, page: int, per_page: int = 10):
    """Lấy dữ liệu hóa đơn theo trang kèm thống kê.

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
        tuple: (pagination, invoices, total_invoices, cho_xac_nhan, dang_xu_ly, da_thanh_toan, da_huy)
    """
    query = build_invoice_query(keyword, status, date_from, date_to, min_value, max_value)

    pagination = query.order_by(Invoice.ma_hoa_don.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    # Thống kê theo trạng thái (loại trừ đã xóa)
    total_invoices = Invoice.query.filter(Invoice.trang_thai != 3).count()
    cho_xac_nhan = Invoice.query.filter_by(trang_thai=0).count()
    dang_xu_ly = Invoice.query.filter_by(trang_thai=1).count()
    da_thanh_toan = Invoice.query.filter_by(trang_thai=2).count()
    da_huy = Invoice.query.filter_by(trang_thai=4).count()

    return (
        pagination,
        pagination.items,
        total_invoices,
        cho_xac_nhan,
        dang_xu_ly,
        da_thanh_toan,
        da_huy,
    )


def get_invoice_or_404(invoice_id: int):
    """Lấy hóa đơn theo id hoặc trả về 404.

    Args:
        invoice_id (int): Mã hóa đơn.

    Returns:
        Invoice: Hóa đơn tìm thấy.
    """
    return Invoice.query.get_or_404(invoice_id)


def create_invoice(ma_tai_khoan: int, tong_tien_tam_tinh: float = None, ngay_dat_hang: str = None, trang_thai: int = 0):
    """Tạo mới hóa đơn và lưu vào cơ sở dữ liệu.

    Args:
        ma_tai_khoan (int): Mã tài khoản.
        tong_tien_tam_tinh (float, optional): Tổng tiền tạm tính.
        ngay_dat_hang (str, optional): Ngày đặt hàng (YYYY-MM-DD).
        trang_thai (int, optional): Trạng thái. Defaults to 0.

    Returns:
        Invoice: Hóa đơn vừa tạo.
    """
    ngay_dat_hang_obj = None
    if ngay_dat_hang:
        try:
            ngay_dat_hang_obj = datetime.strptime(ngay_dat_hang, "%Y-%m-%d")
        except (TypeError, ValueError):
            ngay_dat_hang_obj = datetime.utcnow()
    else:
        ngay_dat_hang_obj = datetime.utcnow()
    
    invoice = Invoice(
        ma_tai_khoan=ma_tai_khoan,
        tong_tien_tam_tinh=tong_tien_tam_tinh,
        ngay_tao=datetime.utcnow(),
        ngay_dat_hang=ngay_dat_hang_obj,
        trang_thai=trang_thai,
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice


def update_invoice(invoice: Invoice, ma_tai_khoan: int = None, tong_tien_tam_tinh: float = None, ngay_dat_hang: str = None, trang_thai: int = None):
    """Cập nhật thông tin hóa đơn.

    Args:
        invoice (Invoice): Hóa đơn cần cập nhật.
        ma_tai_khoan (int, optional): Mã tài khoản mới.
        tong_tien_tam_tinh (float, optional): Tổng tiền tạm tính mới.
        ngay_dat_hang (str, optional): Ngày đặt hàng mới (YYYY-MM-DD).
        trang_thai (int, optional): Trạng thái mới.

    Returns:
        Invoice: Hóa đơn sau khi cập nhật.
    """
    if ma_tai_khoan is not None:
        invoice.ma_tai_khoan = ma_tai_khoan
    
    if tong_tien_tam_tinh is not None:
        invoice.tong_tien_tam_tinh = tong_tien_tam_tinh
    
    if ngay_dat_hang:
        try:
            invoice.ngay_dat_hang = datetime.strptime(ngay_dat_hang, "%Y-%m-%d")
        except (TypeError, ValueError):
            pass
    
    if trang_thai is not None:
        invoice.trang_thai = trang_thai
    
    db.session.commit()
    return invoice


def soft_delete_invoice(invoice: Invoice):
    """Xóa mềm hóa đơn bằng cách đặt trạng thái đã xóa.

    Args:
        invoice (Invoice): Hóa đơn cần xóa.
    """
    invoice.trang_thai = 3  # Trạng thái đã xóa
    db.session.commit()
