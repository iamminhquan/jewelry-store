from app.extensions import db
from datetime import datetime


class Cart(db.Model):
    __tablename__ = "GioHang"

    ma_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_tai_khoan = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )

    ngay_tao = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    ngay_chinh_sua = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    trang_thai = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return f"<GioHang {self.ma_gio_hang} - tai_khoan={self.ma_tai_khoan}>"
