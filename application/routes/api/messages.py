"""/application/routes/api/messages.py"""

import jwt
import os

from flask import Blueprint, request, jsonify
from datetime import datetime
from jwt import ExpiredSignatureError, InvalidTokenError
from extensions import db
from application.models import Message, User, Room

messages_api_bp = Blueprint("messages", __name__, url_prefix="/api/messages")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")

@messages_api_bp.route("/save_message", methods=["POST"])
def save_message():
    print(f"[api/messages.py] Incoming request to save_message")

    # --- Token Extraction & Validation ---
    auth_header = request.headers.get("Authorization")
    print(f"[api/messages.py] auth_header: {auth_header}")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or malformed Authorization header."}), 401

    token = auth_header.split(" ")[1]
    print(f"[api/messages.py] token: {token}")

    # header = jwt.get_unverified_header(token)
    # print("[api/messages.py] JWT header:", header)

    # # Also print body (no verification yet)
    # body = jwt.decode(token, options={"verify_signature": False})
    # print("[api/messages.py] JWT body (unverified):", body)

    try:
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        user_id = decoded_token.get("sub")
        username = decoded_token.get("username")
        print(f"[api/messages.py] decoded_token: {decoded_token}")
    except ExpiredSignatureError:
        print(f"[api/messages.py] ⚠️ Token has expired.")
        return jsonify({"error": "Token has expired."}), 401
    except InvalidTokenError:
        print(f"[api/messages.py] ⚠️ Invalid token.")
        return jsonify({"error": "Invalid token."}), 401
    except Exception as e:
        print(f"[api/messages.py] Unexpected JWT decode error: {e}")
        return jsonify({"error": "Token decoding failed."}), 401
    
    data = request.json
    print(f"[api/messages.py] Incoming data: {data}")

    # Validate basic keys
    required_keys = {"room", "sender", "content", "timestamp"}
    if not data or not required_keys.issubset(data.keys()):
        return {"error": "Missing required fields in request."}, 400

    try:
        room = Room.query.filter_by(name=data["room"]).first()
        if not room:
            return {"error": "Room not found."}, 404
        room_id = room.id
    except Exception as e:
        print(f"[api/messages.py] ⚠️ Room query failed: {e}")
        return {"error": "Internal server error on room lookup."}, 500

    try:
        user = User.query.filter_by(username=data["sender"]).first()
        if not user:
            return {"error": "Sender not found."}, 404
        sender_id = user.id
    except Exception as e:
        print(f"[api/messages.py] ⚠️ User query failed: {e}")
        return {"error": "Internal server error on user lookup."}, 500

    try:
        content = data["content"]
        timestamp = datetime.fromisoformat(data["timestamp"])
    except Exception as e:
        print(f"[api/messages.py] ⚠️ Invalid content or timestamp: {e}")
        return {"error": "Invalid content or timestamp."}, 400

    try:
        message = Message(
            timestamp=timestamp,
            content=content,
            sender_id=sender_id,
            room_id=room_id,
        )
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[api/messages.py] ⚠️ DB commit failed: {e}")
        return {"error": "Failed to save message."}, 500

    return {"status": "saved"}, 200
