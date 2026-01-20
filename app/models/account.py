from flask_login import UserMixin
from sqlalchemy.orm import synonym
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class Account(UserMixin, db.Model):
    __tablename__ = "TaiKhoan"

    ma_tai_khoan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_tai_khoan = db.Column(db.String(256), nullable=False, unique=True)
    password_hash = db.Column("mat_khau", db.String(256), nullable=False)
    mat_khau = synonym("password_hash")
    ho_ten = db.Column(db.String(256), nullable=False)
    ngay_sinh = db.Column(db.DateTime, nullable=False)
    gioi_tinh = db.Column(db.SmallInteger, nullable=False)
    so_dien_thoai = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    dia_chi = db.Column(db.String(256), nullable=False)
    trang_thai = db.Column(db.SmallInteger, nullable=False)
    role = db.Column(db.SmallInteger, nullable=False)

    def get_id(self):
        return str(self.ma_tai_khoan)

    @property
    def is_active(self):
        return self.trang_thai == 1

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<Account {self.ten_tai_khoan}>"


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))
