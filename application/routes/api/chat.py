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

    try:
        user = get_user_from_id(id)
    except Exception as e:
        print(f"[chat_history] ⚠️ Error fetching user from DB: {e}")
        return "Internal server error while fetching user.", 500

    if not user:
        return "User not found.", 404
    try:
        room_name = request.args.get("room", "general")
        before = request.args.get("before", None)
        limit = int(request.args.get("limit", 50))
    except ValueError as e:
        print(f"[chat_history] ⚠️ Invalid query parameter: {e}")
        return "Invalid query parameters.", 400
        
    try:
        room = Room.query.filter(Room.name==room_name).first()
        room_id = room.id if room else None
        print(f"[api/chat] room_id: {room_id}")
    except Exception as e:
        print(f"[chat_history] ⚠️ Error fetching user from DB: {e}")
        return "Internal server error while fetching user.", 500
    try:
        query = Message.query.filter_by(room_id=room_id)

        if before:
            from datetime import datetime
            before_dt = datetime.fromisoformat(before)
            query = query.filter(Message.timestamp < before_dt)
        
        
        messages = query.order_by(desc(Message.timestamp)).limit(limit).all()
    except Exception as e:
        print(f"[chat_history] ⚠️ Error querying messages: {e}")
        return "Error loading chat history.", 500

    chat_history = []
    for msg in messages:
        try:
            chat_history.append({
                "id": msg.id,
                "timestamp": msg.timestamp,
                "content": msg.content,
                "sender": msg.sender.username,
            })
        except Exception as e:
            print(f"[chat_history] ⚠️ Error serializing message: {e}")
            continue

    return chat_history

