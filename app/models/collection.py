from app.extensions import db


class Collection(db.Model):
    __tablename__ = "BoSuuTap"

    ma_bo_suu_tap = db.Column(db.Integer, primary_key=True)
    ten_bo_suu_tap = db.Column(db.String(256), nullable=False)
    mo_ta = db.Column(db.Text)
    trang_thai = db.Column(db.SmallInteger)
