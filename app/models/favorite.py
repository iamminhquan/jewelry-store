"""
Model Sản phẩm yêu thích (Favorite/Wishlist).
"""

from datetime import datetime
from app.extensions import db


class Favorite(db.Model):
    __tablename__ = "SanPhamYeuThich"

    ma_yeu_thich = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    ma_tai_khoan = db.Column(
        db.Integer, 
        db.ForeignKey("TaiKhoan.ma_tai_khoan"), 
        nullable=False
    )
    
    ma_san_pham = db.Column(
        db.Integer, 
        db.ForeignKey("SanPham.ma_san_pham"), 
        nullable=False
    )
    
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    product = db.relationship("Product", backref="favorites", lazy=True)

    # Unique constraint - mỗi user chỉ có thể yêu thích 1 sản phẩm 1 lần
    __table_args__ = (
        db.UniqueConstraint('ma_tai_khoan', 'ma_san_pham', name='unique_user_product_favorite'),
    )

    def __init__(self, user_id, product_id):
        self.ma_tai_khoan = user_id
        self.ma_san_pham = product_id
