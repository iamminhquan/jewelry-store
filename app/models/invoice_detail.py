from datetime import datetime
from app.extensions import db


class InvoiceDetail(db.Model):
    __tablename__ = "ChiTietHoaDon"

    ma_chi_tiet_hoa_don = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_hoa_don = db.Column(
        db.Integer,
        db.ForeignKey("HoaDon.ma_hoa_don"),
        nullable=False,
    )

    ma_san_pham = db.Column(
        db.Integer,
        db.ForeignKey("SanPham.ma_san_pham"),
        nullable=False,
    )

    so_luong = db.Column(db.Integer, nullable=False)
    don_gia = db.Column(db.Numeric(10, 2))
    thanh_tien = db.Column(db.Numeric(10, 2))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)

    # ===== Relationships =====
    san_pham = db.relationship(
        "Product",
        backref=db.backref("chi_tiet_hoa_dons", lazy=True),
    )
