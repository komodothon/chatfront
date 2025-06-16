"""/application/routes/api/messages.py"""

from flask import Blueprint, request
from datetime import datetime

from extensions import db

from application.models import Message, User, Room

messages_api_bp = Blueprint("messages", __name__, url_prefix="/api/messages")

@messages_api_bp.route("/save_message", methods=["POST"])
def save_message():
    data = request.json
    # print(f"[api/messages.py]data: {data}")
    print()
    room = Room.query.filter_by(name=data["room"]).first()
    if room:
        room_id = room.id

        # print(f"[api/messages.py]: room_id: {room_id}")


    user = User.query.filter_by(username=data["sender"]).first()
    if user:
        sender_id = user.id

        # print(f"[api/messages.py]: sender_id: {sender_id}")

    content = data["content"]
    timestamp = datetime.fromisoformat(data["timestamp"])

    message = Message(
        timestamp=timestamp,
        content=content,
        sender_id=sender_id,
        room_id=room_id,
    )

    db.session.add(message)
    db.session.commit()

    # print(f"[api/messages.py]{message.to_dict()}")

    return {"status": "saved"}, 200