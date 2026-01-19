from app.extensions import db


class Material(db.Model):
    __tablename__ = "ChatLieu"

    ma_chat_lieu = db.Column(db.Integer, primary_key=True)
    ten_chat_lieu = db.Column(db.String(256), nullable=False)
