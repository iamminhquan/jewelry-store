from app.extensions import db


class CartDetail(db.Model):
    __tablename__ = "ChiTietGioHang"

    def __init__(
        self,
        cart_detail_id,
        product_id,
        quantity,
        price_at,
        created_at,
    ) -> None:
        self.__cart_detail_id = cart_detail_id
        self.__product_id = product_id
        self.__quantity = quantity
        self.__price_at = price_at
        self.__created_at = created_at

    ma_chi_tiet_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_gio_hang = db.Column(db.Integer, nullable=False)

    ma_san_pham = db.Column(db.Integer, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=True)

    gia_tai_thoi_diem = db.Column(db.Numeric(10, 2))
