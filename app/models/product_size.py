from app.extensions import db


class ProductSize(db.Model):
    __tablename__ = "KichThuocSanPham"

    ma_kich_thuoc_san_pham = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )

    ma_san_pham = db.Column(db.Integer, nullable=False)

    ten_kich_thuoc = db.Column(db.Float, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False, server_default="0")
