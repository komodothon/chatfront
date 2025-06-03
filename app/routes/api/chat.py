"""/app/routes/api/chat.py"""

# from flask import Blueprint, request
# from flask_jwt_extended import jwt_required

# from app.models import Message

# chat_api_bp = Blueprint("chat_api", __name__, url_prefix="/api")

# @chat_api_bp.route("/chat_history", methods=["GET"])
# @jwt_required()
# def chat_history():
#     room = request.args.get("room", "general")
#     before = request.args.get("before", None)
#     limit = int(request.args.get("limit", 20))

#     chat_history = Message.query.filter_by(chat_id=chat.)
