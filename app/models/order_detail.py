from app.extensions import db
from datetime import datetime


class OrderDetail(db.Model):
    __tablename__ = "ChiTietDonHang"

    ma_chi_tiet_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_don_hang = db.Column(
        db.Integer, db.ForeignKey("DonHang.ma_don_hang"), nullable=False
    )

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    so_luong = db.Column(db.Integer, nullable=False)

    don_gia = db.Column(db.Numeric(10, 2), nullable=True)

    thanh_tien = db.Column(db.Numeric(10, 2), nullable=True)

    ngay_tao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<ChiTietDonHang "
            f"id={self.ma_chi_tiet_don_hang} "
            f"don_hang={self.ma_don_hang} "
            f"san_pham={self.ma_san_pham}>"
        )
