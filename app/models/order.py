from datetime import datetime

from app.extensions import db


class Order(db.Model):
    __tablename__ = "DonHang"

    ma_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ma_tai_khoan = db.Column(db.Integer, nullable=False)

    tong_tien_tam_tinh = db.Column(db.Numeric(10, 2))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_dat_hang = db.Column(db.DateTime)

    trang_thai = db.Column(db.SmallInteger)

    # 1 đơn hàng - nhiều chi tiết đơn hàng
    chi_tiet_don_hang = db.relationship(
        "OrderDetail",
        backref="don_hang",
        lazy=True
    )

    def __repr__(self):
        return f"<DonHang {self.ma_don_hang}>"
