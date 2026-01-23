from app.extensions import db
from datetime import datetime


class OrderDetail(db.Model):
    __tablename__ = "ChiTietDonHang"

    def __init__(
        self,
        order_detail_id,
        product_id,
        quantity,
        price,
        total_fee,
    ) -> None:
        self.ma_don_hang = order_detail_id
        self.ma_san_pham = product_id
        self.so_luong = quantity
        self.don_gia = price
        self.thanh_tien = total_fee

    ma_chi_tiet_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_don_hang = db.Column(
        db.Integer, db.ForeignKey("DonHang.ma_don_hang"), nullable=False
    )

    ma_san_pham = db.Column(db.Integer, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False)
    don_gia = db.Column(db.Numeric(10, 2))
    thanh_tien = db.Column(db.Numeric(10, 2))

    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChiTietDonHang {self.ma_chi_tiet_don_hang}>"
