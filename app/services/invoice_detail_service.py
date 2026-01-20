from app.models.invoice_detail import InvoiceDetail
from app.models.product import Product


def get_invoice_details_by_invoice_id(invoice_id: int):
    """Lấy tất cả chi tiết hóa đơn theo mã hóa đơn.

    Args:
        invoice_id (int): Mã hóa đơn.

    Returns:
        list: Danh sách chi tiết hóa đơn.
    """
    return InvoiceDetail.query.filter_by(ma_hoa_don=invoice_id).all()


def get_invoice_detail_with_product(invoice_id: int):
    """Lấy chi tiết hóa đơn kèm thông tin sản phẩm.

    Args:
        invoice_id (int): Mã hóa đơn.

    Returns:
        list: Danh sách chi tiết hóa đơn với thông tin sản phẩm.
    """
    invoice_details = InvoiceDetail.query.filter_by(ma_hoa_don=invoice_id).all()
    
    # Thêm thông tin sản phẩm vào mỗi chi tiết
    result = []
    for detail in invoice_details:
        product = Product.query.get(detail.ma_san_pham)
        result.append({
            'detail': detail,
            'product': product
        })
    
    return result


def get_invoice_detail_or_404(invoice_detail_id: int):
    """Lấy chi tiết hóa đơn theo id hoặc trả về 404.

    Args:
        invoice_detail_id (int): Mã chi tiết hóa đơn.

    Returns:
        InvoiceDetail: Chi tiết hóa đơn tìm thấy.
    """
    return InvoiceDetail.query.get_or_404(invoice_detail_id)


def create_invoice_detail(ma_hoa_don: int, ma_san_pham: int, so_luong: int, don_gia: float, thanh_tien: float = None):
    """Tạo mới chi tiết hóa đơn.

    Args:
        ma_hoa_don (int): Mã hóa đơn.
        ma_san_pham (int): Mã sản phẩm.
        so_luong (int): Số lượng.
        don_gia (float): Đơn giá.
        thanh_tien (float, optional): Thành tiền. Nếu None sẽ tính tự động.

    Returns:
        InvoiceDetail: Chi tiết hóa đơn vừa tạo.
    """
    from datetime import datetime
    from app.extensions import db
    
    if thanh_tien is None:
        thanh_tien = float(so_luong) * float(don_gia)
    
    invoice_detail = InvoiceDetail(
        ma_hoa_don=ma_hoa_don,
        ma_san_pham=ma_san_pham,
        so_luong=so_luong,
        don_gia=don_gia,
        thanh_tien=thanh_tien,
        ngay_tao=datetime.utcnow(),
    )
    db.session.add(invoice_detail)
    db.session.commit()
    return invoice_detail


def update_invoice_detail(invoice_detail: InvoiceDetail, so_luong: int = None, don_gia: float = None):
    """Cập nhật chi tiết hóa đơn.

    Args:
        invoice_detail (InvoiceDetail): Chi tiết hóa đơn cần cập nhật.
        so_luong (int, optional): Số lượng mới.
        don_gia (float, optional): Đơn giá mới.

    Returns:
        InvoiceDetail: Chi tiết hóa đơn sau khi cập nhật.
    """
    from app.extensions import db
    
    if so_luong is not None:
        invoice_detail.so_luong = so_luong
    
    if don_gia is not None:
        invoice_detail.don_gia = don_gia
    
    # Tự động tính lại thành tiền
    if so_luong is not None or don_gia is not None:
        invoice_detail.thanh_tien = float(invoice_detail.so_luong) * float(invoice_detail.don_gia)
    
    db.session.commit()
    return invoice_detail


def delete_invoice_detail(invoice_detail: InvoiceDetail):
    """Xóa chi tiết hóa đơn.

    Args:
        invoice_detail (InvoiceDetail): Chi tiết hóa đơn cần xóa.
    """
    from app.extensions import db
    db.session.delete(invoice_detail)
    db.session.commit()
