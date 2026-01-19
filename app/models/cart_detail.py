from app.extensions import db


class CartDetail(db.Model):
    __tablename__ = "ChiTietGioHang"

    ma_chi_tiet_gio_hang = db.Column(db.Integer, primary_key=True)

    ma_gio_hang = db.Column(
        db.Integer, db.ForeignKey("GioHang.ma_gio_hang"), nullable=False
    )

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    so_luong = db.Column(db.Integer, nullable=False)
