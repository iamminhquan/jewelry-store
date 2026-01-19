from app.extensions import db


class ProductMaterial(db.Model):
    __tablename__ = "SanPham__ChatLieu"

    ma_san_pham = db.Column(db.Integer, primary_key=True)

    ma_chat_lieu = db.Column(db.Integer, primary_key=True)
