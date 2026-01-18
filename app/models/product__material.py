from app.extensions import db

SanPham__ChatLieu = db.Table(
    "SanPham__ChatLieu",
    db.Column(
        "ma_san_pham",
        db.Integer,
        db.ForeignKey("SanPham.ma_san_pham"),
        primary_key=True,
    ),
    db.Column(
        "ma_chat_lieu",
        db.Integer,
        db.ForeignKey("ChatLieu.ma_chat_lieu"),
        primary_key=True,
    ),
)
