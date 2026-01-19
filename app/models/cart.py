from app.extensions import db


class Cart(db.Model):
    __tablename__ = "GioHang"

    ma_gio_hang = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_tai_khoan = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=True)

    ngay_chinh_sua = db.Column(db.DateTime, nullable=True)

    trang_thai = db.Column(db.SmallInteger)
