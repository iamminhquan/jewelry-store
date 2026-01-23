from datetime import datetime
from app.extensions import db


class Contact(db.Model):
    __tablename__ = "LienHe"

    ma_lien_he = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ten_khach_hang = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    so_dien_thoai = db.Column(db.String(11), nullable=False)

    noi_dung = db.Column(db.Text, nullable=False)

    ma_tai_khoan = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=True
    )

    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
