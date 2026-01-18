from app.extensions import db


class Category(db.Model):
    __tablename__ = "DanhMuc"

    ma_danh_muc = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ten_danh_muc = db.Column(db.String(256), nullable=False)

    mo_ta = db.Column(db.Text, nullable=True)

    trang_thai = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return f"<DanhMuc {self.ma_danh_muc} - {self.ten_danh_muc}>"
