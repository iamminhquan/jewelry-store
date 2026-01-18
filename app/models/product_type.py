from app.extensions import db


class ProductType(db.Model):
    __tablename__ = "LoaiSanPham"

    ma_loai_san_pham = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ten_loai_san_pham = db.Column(db.String(256), nullable=False)

    ma_danh_muc = db.Column(
        db.Integer, db.ForeignKey("DanhMuc.ma_danh_muc"), nullable=False
    )

    slug = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f"<LoaiSanPham {self.ma_loai_san_pham} - {self.ten_loai_san_pham}>"
