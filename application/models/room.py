"""/application/models/room.py"""

from extensions import db
from application.models.base import BaseModel

class Room(BaseModel):
    __tablename__ = "rooms"

    # BaseModel provides: id, name, description, created_at, updated_at (if you added those)

    messages = db.relationship("Message", back_populates="room", cascade="all, delete-orphan")

    def to_safe_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }