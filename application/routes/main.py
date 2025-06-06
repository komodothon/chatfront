"""/application/routes/main.py"""

from flask import Blueprint, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.models import User

main_bp = Blueprint("main", __name__, url_prefix="/main")

@main_bp.route("/", methods=["GET"])
@jwt_required()
def home():
    id = get_jwt_identity()

    # Print JWT token from Authorization header or cookie
    # auth_header = request.headers.get("Authorization", None)
    # access_cookie = request.cookies.get("access_token_cookie")  # default cookie name by Flask-JWT-Extended

    # print("Authorization header:", auth_header)
    # print("Access token cookie:", access_cookie)

    user = User.query.get(id)

    if not user:
        return "User not found.", 404
    
    username = user.username

    return render_template("home.html", username=username)