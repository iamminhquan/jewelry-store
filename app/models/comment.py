from app.extensions import db


class Comment(db.Model):
    __tablename__ = "DanhGia"

    ma_danh_gia = db.Column(db.Integer, primary_key=True)

    ma_san_pham = db.Column(
        db.Integer, db.ForeignKey("SanPham.ma_san_pham"), nullable=False
    )

    nguoi_danh_gia = db.Column(
        db.Integer, db.ForeignKey("TaiKhoan.ma_tai_khoan"), nullable=False
    )

    noi_dung = db.Column(db.Text)
