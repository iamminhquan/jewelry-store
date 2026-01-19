from datetime import datetime

from app.extensions import db


class ProductImage(db.Model):
    __tablename__ = "HinhAnhSanPham"

    ma_hinh_anh = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    duong_dan = db.Column(db.String(256), nullable=False)

    anh_chinh = db.Column(db.SmallInteger, nullable=False, default=0)

    thu_tu_sap_xep = db.Column(db.Integer, nullable=True)

    ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    san_pham = db.relationship("Products", back_populates="hinh_anhs")

    def __repr__(self):
        return f"<HinhAnhSanPham {self.ma_hinh_anh} - SP {self.ma_san_pham}>"
