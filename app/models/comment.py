from app.extensions import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = "DanhGia"

    ma_danh_gia = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    noi_dung = db.Column(db.Text, nullable=True)

    nguoi_danh_gia = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )

    ngay_tao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    ngay_chinh_sua = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    trang_thai = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return (
            f"<DanhGia {self.ma_danh_gia} "
            f"san_pham={self.ma_san_pham} "
            f"nguoi_danh_gia={self.nguoi_danh_gia}>"
        )
