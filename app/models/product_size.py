from app.extensions import db


class ProductSize(db.Model):
    __tablename__ = "KichThuocSanPham"

    ma_kich_thuoc_san_pham = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_san_pham = db.Column(
        db.Integer,
        nullable=False,
        # Nếu có FK sau này:
        # db.ForeignKey('SanPham.ma_san_pham')
    )

    ten_kich_thuoc = db.Column(db.Float, nullable=False)

    so_luong = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return (
            f"<KichThuocSanPham "
            f"id={self.ma_kich_thuoc_san_pham}, "
            f"san_pham={self.ma_san_pham}, "
            f"kich_thuoc={self.ten_kich_thuoc}>"
        )
