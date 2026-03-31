from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    telegram_message_id = db.Column(db.String(100), nullable=True)
    chat_id = db.Column(db.String(100), nullable=True)
    sender_name = db.Column(db.String(255), nullable=True)
    message_text = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False, default="Normal")
    reason = db.Column(db.Text, nullable=True)
    confidence = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "telegram_message_id": self.telegram_message_id,
            "chat_id": self.chat_id,
            "sender_name": self.sender_name,
            "message_text": self.message_text,
            "category": self.category,
            "reason": self.reason,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat(),
        }