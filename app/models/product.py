from datetime import datetime

from app.extensions import db


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

    hinh_anhs = db.relationship(
        "ProductImage",
        back_populates="san_pham",
        cascade="all, delete-orphan",
        lazy="select",
    )

    @property
    def anh_chinh(self) -> str:
        """Lấy đường dẫn hình ảnh chính của sản phẩm.
        
        Ưu tiên: ảnh có anh_chinh=1 > ảnh đầu tiên theo thứ tự > ảnh mặc định
        
        Returns:
            str: Đường dẫn hình ảnh (không bao gồm 'static/')
        """
        if not self.hinh_anhs:
            return "images/product/default.png"
        
        # Tìm ảnh chính (anh_chinh = 1)
        for img in self.hinh_anhs:
            if img.anh_chinh == 1:
                return img.duong_dan
        
        # Nếu không có ảnh chính, lấy ảnh đầu tiên theo thứ tự sắp xếp
        sorted_images = sorted(
            self.hinh_anhs, 
            key=lambda x: (x.thu_tu_sap_xep or 999, x.ma_hinh_anh)
        )
        return sorted_images[0].duong_dan if sorted_images else "images/product/default.png"

    @property
    def tat_ca_hinh_anh(self) -> list:
        """Lấy tất cả hình ảnh của sản phẩm, sắp xếp theo thứ tự.
        
        Returns:
            list: Danh sách đường dẫn hình ảnh
        """
        if not self.hinh_anhs:
            return []
        
        sorted_images = sorted(
            self.hinh_anhs,
            key=lambda x: (x.thu_tu_sap_xep or 999, x.ma_hinh_anh)
        )
        return [img.duong_dan for img in sorted_images]

    def __repr__(self):
        return f"<SanPham {self.ma_san_pham} - {self.ten_san_pham}>"
