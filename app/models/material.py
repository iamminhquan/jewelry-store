from app.extensions import db


class Material(db.Model):
    __tablename__ = "ChatLieu"

    ma_chat_lieu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ten_chat_lieu = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<ChatLieu {self.ma_chat_lieu} - {self.ten_chat_lieu}>"
