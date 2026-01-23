from app.extensions import db


class InvoiceDetail(db.Model):
    __tablename__ = "ChiTietHoaDon"

    ma_chi_tiet_hoa_don = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )

    ma_hoa_don = db.Column(db.Integer, db.ForeignKey("HoaDon.ma_hoa_don"), nullable=False)

    ma_san_pham = db.Column(db.Integer, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False)

    don_gia = db.Column(db.Numeric(10, 2))

    thanh_tien = db.Column(db.Numeric(10, 2))

    ngay_tao = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<ChiTietHoaDon {self.ma_chi_tiet_hoa_don}>"
