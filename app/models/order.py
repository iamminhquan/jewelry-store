from app.extensions import db


class Order(db.Model):
    __tablename__ = "DonHang"

    ma_don_hang = db.Column(db.Integer, primary_key=True)

    ma_tai_khoan = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )

    tong_tien_tam_tinh = db.Column(db.Numeric(10, 2))
