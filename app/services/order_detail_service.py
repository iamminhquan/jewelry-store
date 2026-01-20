from app.models.order_detail import OrderDetail
from app.models.product import Product


def get_order_details_by_order_id(order_id: int):
    """Lấy tất cả chi tiết đơn hàng theo mã đơn hàng.

    Args:
        order_id (int): Mã đơn hàng.

    Returns:
        list: Danh sách chi tiết đơn hàng.
    """
    return OrderDetail.query.filter_by(ma_don_hang=order_id).all()


def get_order_detail_with_product(order_id: int):
    """Lấy chi tiết đơn hàng kèm thông tin sản phẩm.

    Args:
        order_id (int): Mã đơn hàng.

    Returns:
        list: Danh sách chi tiết đơn hàng với thông tin sản phẩm.
    """
    order_details = OrderDetail.query.filter_by(ma_don_hang=order_id).all()
    
    # Thêm thông tin sản phẩm vào mỗi chi tiết
    result = []
    for detail in order_details:
        product = Product.query.get(detail.ma_san_pham)
        result.append({
            'detail': detail,
            'product': product
        })
    
    return result


def get_order_detail_or_404(order_detail_id: int):
    """Lấy chi tiết đơn hàng theo id hoặc trả về 404.

    Args:
        order_detail_id (int): Mã chi tiết đơn hàng.

    Returns:
        OrderDetail: Chi tiết đơn hàng tìm thấy.
    """
    return OrderDetail.query.get_or_404(order_detail_id)
