"""/application/models/message.py"""


from extensions import db
from application.models.base import BaseModel
from sqlalchemy.sql import func

class Message(BaseModel):
    __tablename__ = "messages"

    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    content = db.Column(db.String(1000), nullable=False)

    # Sender
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages", uselist=False)

    # Optional receiver (for direct messages)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_messages", uselist=False)

    # Optional room (for room-based chat)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id", ondelete="SET NULL"), nullable=True)
    room = db.relationship("Room", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "content": self.content,
            "sender": self.sender.to_safe_dict() if self.sender else None,
            "receiver": self.receiver.to_safe_dict() if self.receiver else None,
            "room": self.room.to_safe_dict() if self.room else None
        }

    def __repr__(self):
        return f"<Message {self.id} from {self.sender_id} to {self.receiver_id}>"        
