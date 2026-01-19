from app.extensions import db


class ProductImage(db.Model):
    __tablename__ = "HinhAnhSanPham"

    ma_hinh_anh = db.Column(db.Integer, primary_key=True)

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    duong_dan = db.Column(db.String(256), nullable=False)
    anh_chinh = db.Column(db.SmallInteger, default=0)
