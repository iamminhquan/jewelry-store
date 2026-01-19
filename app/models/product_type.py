from app.extensions import db


class ProductType(db.Model):
    __tablename__ = "LoaiSanPham"

    ma_loai_san_pham = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )

    ten_loai_san_pham = db.Column(db.String(256), nullable=False)

    ma_danh_muc = db.Column(db.Integer, nullable=False)

    slug = db.Column(db.String(256), nullable=True)
