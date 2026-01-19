from app.extensions import db


class Cart(db.Model):
    __tablename__ = "GioHang"

    ma_gio_hang = db.Column(db.Integer, primary_key=True)
    ma_tai_khoan = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )
