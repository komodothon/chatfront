"""/application/routes/api/chat.py"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc

from application.models import User, Message, Room
from application.utils import get_user_from_id

chat_api_bp = Blueprint("chat_api", __name__, url_prefix="/api/chat")

@chat_api_bp.route("/chat_history", methods=["GET"])
@jwt_required()
def chat_history():
    id = get_jwt_identity()

    user = get_user_from_id(id)

    if not user:
        return "User not found.", 404
    
    room_name = request.args.get("room", "general")
    before = request.args.get("before", None)
    limit = int(request.args.get("limit", 50))

    room = Room.query.filter(Room.name==room_name).first()
    room_id = room.id if room else None
    print(f"[api/chat] room_id: {room_id}")
    
    query = Message.query.filter_by(room_id=room_id)

    if before:
        from datetime import datetime
        before_dt = datetime.fromisoformat(before)
        query = query.filter(Message.timestamp < before_dt)
    
    
    messages = query.order_by(desc(Message.timestamp)).limit(limit).all()

    chat_history = [{
        "id": message.id,
        "timestamp": message.timestamp,
        "content": message.content,
        "sender": message.sender.username,
    } for message in messages]

    return chat_history

