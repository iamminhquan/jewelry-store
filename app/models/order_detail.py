from app.extensions import db


class OrderDetail(db.Model):
    __tablename__ = "ChiTietDonHang"

    ma_chi_tiet_don_hang = db.Column(db.Integer, primary_key=True)

    ma_don_hang = db.Column(
        db.Integer, db.ForeignKey("DonHang.ma_don_hang"), nullable=False
    )

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    so_luong = db.Column(db.Integer, nullable=False)
