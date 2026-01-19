from app.extensions import db


class CartDetail(db.Model):
    __tablename__ = "ChiTietGioHang"

    ma_chi_tiet_gio_hang = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )

    ma_gio_hang = db.Column(db.Integer, nullable=False)

    ma_san_pham = db.Column(db.Integer, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=True)

    gia_tai_thoi_diem = db.Column(db.Numeric(10, 2))
