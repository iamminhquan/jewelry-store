from app.extensions import db


class Account(db.Model):
    __tablename__ = "TaiKhoan"

    ma_tai_khoan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_tai_khoan = db.Column(db.String(256), nullable=False)
    mat_khau = db.Column(db.String(256), nullable=False)
    ho_ten = db.Column(db.String(256), nullable=False)
    ngay_sinh = db.Column(db.DateTime, nullable=False)
    gioi_tinh = db.Column(db.SmallInteger, nullable=False)
    so_dien_thoai = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    dia_chi = db.Column(db.String(256), nullable=False)
    trang_thai = db.Column(db.SmallInteger, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)

    def __repr__(self):
        return f"<Account {self.ten_tai_khoan}>"
