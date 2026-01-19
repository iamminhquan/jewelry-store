from datetime import datetime
from app.extensions import db


class Invoice(db.Model):
    __tablename__ = "HoaDon"

    ma_hoa_don = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_tai_khoan = db.Column(
        db.Integer,
        db.ForeignKey("TaiKhoan.ma_tai_khoan"),
        nullable=False,
    )

    tong_tien_tam_tinh = db.Column(db.Numeric(10, 2))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_dat_hang = db.Column(db.DateTime)
    trang_thai = db.Column(db.SmallInteger)

    tai_khoan = db.relationship(
        "Account",
        backref=db.backref("hoa_dons", lazy=True),
    )

    chi_tiet_hoa_dons = db.relationship(
        "InvoiceDetail",
        backref="hoa_don",
        cascade="all, delete-orphan",
        lazy=True,
    )
