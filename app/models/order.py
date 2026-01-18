from app.extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "DonHang"

    ma_don_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_tai_khoan = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )

    tong_tien_tam_tinh = db.Column(db.Numeric(10, 2), nullable=True)

    ngay_tao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    ngay_dat_hang = db.Column(db.DateTime, nullable=True)

    trang_thai = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return f"<DonHang {self.ma_don_hang} - tai_khoan={self.ma_tai_khoan}>"
