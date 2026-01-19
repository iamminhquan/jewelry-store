from datetime import datetime

from app.extensions import db
from .product__material import Product__Material


class Product(db.Model):
    __tablename__ = "SanPham"

    ma_san_pham = db.Column(db.Integer, primary_key=True)
    ten_san_pham = db.Column(db.String(256), nullable=False)

    gia_nhap = db.Column(db.Numeric(10, 2), nullable=False)
    gia_xuat = db.Column(db.Numeric(10, 2), nullable=False)

    trong_luong = db.Column(db.Float, nullable=False)
    gioi_tinh = db.Column(db.SmallInteger, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)

    don_vi_tinh = db.Column(db.String(256), nullable=False)
    trang_thai = db.Column(db.SmallInteger, nullable=False)
    mo_ta = db.Column(db.Text)

    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    ngay_chinh_sua = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    ma_danh_muc = db.Column(db.Integer, db.ForeignKey("DanhMuc.ma_danh_muc"))

    ma_loai_san_pham = db.Column(
        db.Integer, db.ForeignKey("LoaiSanPham.ma_loai_san_pham")
    )

    ma_bo_suu_tap = db.Column(db.Integer, db.ForeignKey("BoSuuTap.ma_bo_suu_tap"))

    ma_thuong_hieu = db.Column(db.Integer, db.ForeignKey("ThuongHieu.ma_thuong_hieu"))

    danh_muc = db.relationship("Category")
    loai_san_pham = db.relationship("ProductType")
    bo_suu_tap = db.relationship("Collection")
    thuong_hieu = db.relationship("Brand")

    chat_lieus = db.relationship(
        "Material", secondary=Product__Material, backref="san_phams"
    )
