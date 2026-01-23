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


def check_ma_don_hang_column_exists():
    """Kiểm tra xem cột ma_don_hang có tồn tại trong bảng HoaDon không.
    
    Returns:
        bool: True nếu cột tồn tại, False nếu không.
    """
    try:
        # Thử truy vấn với cột ma_don_hang
        from sqlalchemy import text
        db.session.execute(text("SELECT ma_don_hang FROM HoaDon LIMIT 1"))
        return True
    except Exception:
        db.session.rollback()
        return False


def get_invoice_by_order_id(order_id: int):
    """Lấy hóa đơn theo mã đơn hàng.

    Args:
        order_id (int): Mã đơn hàng.

    Returns:
        Invoice: Hóa đơn tìm thấy hoặc None nếu không có.
    """
    if not check_ma_don_hang_column_exists():
        return None
    
    try:
        return Invoice.query.filter_by(ma_don_hang=order_id).first()
    except Exception:
        # Column might not exist in database yet
        return None


def create_invoice_from_order(order):
    """Tạo hóa đơn từ đơn hàng đã giao thành công.
    
    Hàm này sẽ kiểm tra xem đơn hàng đã có hóa đơn chưa.
    Nếu chưa có, tạo mới hóa đơn và các chi tiết hóa đơn.
    
    Args:
        order: Đơn hàng cần tạo hóa đơn.
        
    Returns:
        Invoice: Hóa đơn vừa tạo hoặc hóa đơn đã tồn tại.
        bool: True nếu tạo mới, False nếu đã tồn tại.
    """
    from app.models.invoice_detail import InvoiceDetail
    from app.models.product import Product
    
    # Kiểm tra xem cột ma_don_hang có tồn tại không
    has_order_column = check_ma_don_hang_column_exists()
    
    # Kiểm tra xem đơn hàng đã có hóa đơn chưa
    if has_order_column:
        existing_invoice = get_invoice_by_order_id(order.ma_don_hang)
        if existing_invoice:
            return existing_invoice, False
    
    # Tạo hóa đơn mới
    invoice = Invoice(
        ma_tai_khoan=order.ma_tai_khoan,
        tong_tien_tam_tinh=order.tong_tien_tam_tinh,
        ngay_tao=datetime.utcnow(),
        ngay_dat_hang=order.ngay_dat_hang or order.ngay_tao,
        trang_thai=2,  # Đã thanh toán (vì đơn hàng đã giao thành công)
    )
    
    # Nếu cột ma_don_hang tồn tại, set giá trị
    if has_order_column:
        invoice.ma_don_hang = order.ma_don_hang
    
    db.session.add(invoice)
    db.session.flush()  # Để lấy ma_hoa_don
    
    # Tạo chi tiết hóa đơn từ chi tiết đơn hàng
    for order_detail in order.chi_tiet_don_hang:
        invoice_detail = InvoiceDetail(
            ma_hoa_don=invoice.ma_hoa_don,
            ma_san_pham=order_detail.ma_san_pham,
            so_luong=order_detail.so_luong,
            don_gia=order_detail.don_gia,
            thanh_tien=order_detail.thanh_tien,
            ngay_tao=datetime.utcnow(),
        )
        db.session.add(invoice_detail)
    
    db.session.commit()
    return invoice, True


def get_invoices_by_user(user_id: int):
    """Lấy tất cả hóa đơn của một người dùng.

    Args:
        user_id (int): Mã tài khoản người dùng.

    Returns:
        list: Danh sách hóa đơn của người dùng (loại trừ đã xóa).
    """
    return Invoice.query.filter(
        Invoice.ma_tai_khoan == user_id,
        Invoice.trang_thai != 3  # Loại trừ đã xóa
    ).order_by(Invoice.ngay_tao.desc()).all()
