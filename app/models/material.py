from app.extensions import db
from .product__material import SanPham__ChatLieu


class Material(db.Model):
    __tablename__ = "ChatLieu"

    ma_chat_lieu = db.Column(db.Integer, primary_key=True, autoincrement=True)

    ten_chat_lieu = db.Column(db.String(256), nullable=False)

    san_phams = db.relationship(
        "SanPham", secondary=SanPham__ChatLieu, back_populates="chat_lieus"
    )

    def __repr__(self):
        return f"<ChatLieu {self.ma_chat_lieu} - {self.ten_chat_lieu}>"
