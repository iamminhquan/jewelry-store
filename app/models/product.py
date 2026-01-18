from datetime import datetime

from app.extensions import db
from .product__material import SanPham__ChatLieu


class Product(db.Model):
    __tablename__ = "SanPham"

    ma_san_pham = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_san_pham = db.Column(db.String(256), nullable=False)

    gia_nhap = db.Column(db.Numeric(10, 2), nullable=False)
    gia_xuat = db.Column(db.Numeric(10, 2), nullable=False)

    trong_luong = db.Column(db.Float, nullable=False)
    ma_kich_thuoc = db.Column(db.Float, nullable=False)

    gioi_tinh = db.Column(db.SmallInteger, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)

    don_vi_tinh = db.Column(db.String(256), nullable=False)
    trang_thai = db.Column(db.SmallInteger, nullable=False)

    mo_ta = db.Column(db.Text, nullable=True)

    ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ngay_chinh_sua = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    hinh_anh = db.Column(db.Integer, nullable=True)
    ma_danh_muc = db.Column(db.Integer, nullable=True)
    loai_san_pham = db.Column(db.Integer, nullable=True)
    bo_suu_tap = db.Column(db.Integer, nullable=True)
    thuong_hieu = db.Column(db.Integer, nullable=True)

    # Khóa ngoại tới bảng SanPham__ChatLieu.
    chat_lieus = db.relationship(
        "ChatLieu",
        secondary=SanPham__ChatLieu,
        back_populates="san_phams",
    )

    # Tham chiếu tới cột ma_danh_muc ở bảng DanhMuc.
    ma_danh_muc = db.Column(
        db.Integer,
        db.ForeignKey("DanhMuc.ma_danh_muc"),
    )

    # Đặt khóa ngoại.
    danh_muc = db.relationship(
        "DanhMuc",
        backref=db.backref("san_phams", lazy=True),
    )

    def __repr__(self):
        return f"<SanPham {self.ma_san_pham} - {self.ten_san_pham}>"
