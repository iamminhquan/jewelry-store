from app.extensions import db
from datetime import datetime


class CartDetail(db.Model):
    __tablename__ = "ChiTietGioHang"

    ma_chi_tiet_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_gio_hang = db.Column(
        db.Integer, db.ForeignKey("GioHang.ma_gio_hang"), nullable=False
    )

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    so_luong = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    gia_tai_thoi_diem = db.Column(db.Numeric(10, 2), nullable=True)

    def __repr__(self):
        return (
            f"<ChiTietGioHang "
            f"id={self.ma_chi_tiet_gio_hang} "
            f"gio_hang={self.ma_gio_hang} "
            f"san_pham={self.ma_san_pham}>"
        )
