from app.extensions import db


class Invoice(db.Model):
    __tablename__ = "HoaDon"

    ma_hoa_don = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_tai_khoan = db.Column(db.Integer, nullable=False)

    tong_tien_tam_tinh = db.Column(db.Numeric(10, 2))

    ngay_tao = db.Column(db.DateTime, nullable=True)

    ngay_dat_hang = db.Column(db.DateTime, nullable=True)

    trang_thai = db.Column(db.SmallInteger)
