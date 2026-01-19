from app.extensions import db


class Comment(db.Model):
    __tablename__ = "DanhGia"

    ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_san_pham = db.Column(db.Integer, nullable=False)

    noi_dung = db.Column(db.Text, nullable=True)

    nguoi_danh_gia = db.Column(db.Integer, nullable=False)

    ngay_tao = db.Column(db.DateTime, nullable=False)

    ngay_chinh_sua = db.Column(db.DateTime, nullable=False)

    trang_thai = db.Column(db.SmallInteger)
