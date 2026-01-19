from app.extensions import db


class Brand(db.Model):
    __tablename__ = "ThuongHieu"

    ma_thuong_hieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_thuong_hieu = db.Column(db.String(256), nullable=False)
    so_dien_thoai = db.Column(db.String(11))
    email = db.Column(db.String(256))
    dia_chi = db.Column(db.String(256))

    def __repr__(self):
        return f"<ThuongHieu {self.ten_thuong_hieu}>"
