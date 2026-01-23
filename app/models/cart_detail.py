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
        self.ma_gio_hang = cart_detail_id
        self.ma_san_pham = product_id
        self.so_luong = quantity
        self.gia_tai_thoi_diem = price_at
        self.ngay_tao = created_at

    ma_chi_tiet_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_gio_hang = db.Column(db.Integer, nullable=False)

    ma_san_pham = db.Column(db.Integer, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=True)

    gia_tai_thoi_diem = db.Column(db.Numeric(10, 2))
