from app.extensions import db
from app.models.product import Product
from sqlalchemy import or_, cast
from sqlalchemy.types import String


def build_product_query(keyword: str, status: str):
    """Tạo truy vấn sản phẩm theo từ khoá và trạng thái.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).

    Returns:
        BaseQuery: Truy vấn sản phẩm đã áp dụng điều kiện lọc.
    """
    query = Product.query

    if status == "1":
        query = query.filter(Product.trang_thai == 1)
    elif status == "2":
        query = query.filter(Product.trang_thai == 2)
    elif status == "3":
        query = query.filter(Product.trang_thai == 3)
    else:
        query = query.filter(Product.trang_thai != 3)

    if keyword:
        query = query.filter(
            or_(
                cast(Product.ma_san_pham, String).like(f"%{keyword}%"),
                Product.ten_san_pham.ilike(f"%{keyword}%"),
            )
        )

    return query


def get_product_page(keyword: str, status: str, page: int, per_page: int = 3):
    """Lấy dữ liệu sản phẩm theo trang kèm thống kê.

    Args:
        keyword (str): Từ khoá tìm kiếm.
        status (str): Trạng thái lọc (1, 2, 3 hoặc None).
        page (int): Trang hiện tại.
        per_page (int, optional): Số bản ghi mỗi trang. Defaults to 3.

    Returns:
        tuple: (pagination, products, total_products, con_hang, het_hang,
        ten_sp_noi_bat)
    """
    query = build_product_query(keyword, status)

    pagination = query.order_by(Product.ma_san_pham.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    total_products = Product.query.filter(Product.trang_thai != 3).count()
    con_hang = Product.query.filter_by(trang_thai=1).count()
    het_hang = Product.query.filter_by(trang_thai=2).count()

    san_pham_noi_bat = Product.query.filter(Product.trang_thai != 3).limit(3).all()
    ten_sp_noi_bat = ", ".join(sp.ten_san_pham for sp in san_pham_noi_bat)

    return (
        pagination,
        pagination.items,
        total_products,
        con_hang,
        het_hang,
        ten_sp_noi_bat,
    )


def get_product_or_404(product_id: int):
    """Lấy sản phẩm theo id hoặc trả về 404.

    Args:
        product_id (int): Mã sản phẩm.

    Returns:
        Product: Sản phẩm tìm thấy.
    """
    return Product.query.get_or_404(product_id)


def create_product(
    ten_san_pham: str,
    gia_nhap,
    gia_xuat,
    trong_luong,
    ma_kich_thuoc,
    gioi_tinh,
    so_luong,
    don_vi_tinh: str,
    trang_thai: int,
    mo_ta: str,
):
    """Tạo mới sản phẩm và lưu vào cơ sở dữ liệu.

    Args:
        ten_san_pham (str): Tên sản phẩm.
        gia_nhap: Giá nhập.
        gia_xuat: Giá xuất.
        trong_luong: Trọng lượng.
        ma_kich_thuoc: Mã kích thước.
        gioi_tinh: Giới tính.
        so_luong: Số lượng.
        don_vi_tinh (str): Đơn vị tính.
        trang_thai (int): Trạng thái sản phẩm.
        mo_ta (str): Mô tả sản phẩm.

    Returns:
        Product: Sản phẩm vừa tạo.
    """
    product = Product(
        ten_san_pham=ten_san_pham,
        gia_nhap=gia_nhap,
        gia_xuat=gia_xuat,
        trong_luong=trong_luong,
        ma_kich_thuoc=ma_kich_thuoc,
        gioi_tinh=gioi_tinh,
        so_luong=so_luong,
        don_vi_tinh=don_vi_tinh,
        trang_thai=trang_thai,
        mo_ta=mo_ta,
    )
    db.session.add(product)
    db.session.commit()
    return product


def update_product(
    product: Product,
    ten_san_pham: str,
    gia_nhap,
    gia_xuat,
    trong_luong,
    ma_kich_thuoc,
    gioi_tinh,
    so_luong,
    don_vi_tinh: str,
    new_status: int,
    mo_ta: str,
):
    """Cập nhật thông tin sản phẩm và lưu thay đổi.

    Args:
        product (Product): Sản phẩm cần cập nhật.
        ten_san_pham (str): Tên sản phẩm.
        gia_nhap: Giá nhập.
        gia_xuat: Giá xuất.
        trong_luong: Trọng lượng.
        ma_kich_thuoc: Mã kích thước.
        gioi_tinh: Giới tính.
        so_luong: Số lượng.
        don_vi_tinh (str): Đơn vị tính.
        new_status (int): Trạng thái mới.
        mo_ta (str): Mô tả sản phẩm.

    Returns:
        Product: Sản phẩm sau khi cập nhật.
    """
    product.ten_san_pham = ten_san_pham
    product.gia_nhap = gia_nhap
    product.gia_xuat = gia_xuat
    product.trong_luong = trong_luong
    product.ma_kich_thuoc = ma_kich_thuoc
    product.gioi_tinh = gioi_tinh
    product.so_luong = so_luong
    product.don_vi_tinh = don_vi_tinh
    product.trang_thai = 3 if new_status == 3 else new_status
    product.mo_ta = mo_ta

    db.session.commit()
    return product


def soft_delete_product(product: Product):
    """Xoá mềm sản phẩm bằng cách đặt trạng thái đã xoá.

    Args:
        product (Product): Sản phẩm cần xoá.
    """
    product.trang_thai = 3
    db.session.commit()
