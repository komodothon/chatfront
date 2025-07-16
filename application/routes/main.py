"""/application/routes/main.py"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta

from application.models import User
from application.utils import get_user_from_id

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.login"))

@main_bp.route("/home", methods=["GET"])
@jwt_required()
def home():
    id = get_jwt_identity()

    # Print JWT token from Authorization header or cookie
    # auth_header = request.headers.get("Authorization", None)
    # access_cookie = request.cookies.get("access_token_cookie")  # default cookie name by Flask-JWT-Extended

    # print("Authorization header:", auth_header)
    # print("Access token cookie:", access_cookie)
    print(f"[main.py] JWT identity: {id}")

    try:
        user = get_user_from_id(id)
    except Exception as e:
        print(f"[main.py] ⚠️ Error fetching user from DB: {e}")
        return "Internal server error while fetching user.", 500

    if not user:
        return "User not found.", 404

    try:
        username = user.username

        ws_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "scope": "websocket",
                "username": username,
            },
            expires_delta=timedelta(minutes=5)
        )
    except Exception as e:
        print(f"[main.py] ⚠️ Error creating WebSocket token: {e}")
        return "Failed to create session token.", 500

    print(f"[main.py] ws_token: {ws_token}")
    return render_template("home.html", username=username, ws_token=ws_token)
