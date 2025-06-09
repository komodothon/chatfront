"""/test1.py"""

from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt, jwt_required
from datetime import timedelta

from application import create_app
import jwt

app = create_app()

id = 4

with app.app_context():
    ws_token = create_access_token(
        identity=str(id),
        additional_claims={"scope": "websocket"},
        expires_delta=timedelta(minutes=2)
    )

    decoded = jwt.decode(
        ws_token,
        key=app.config["JWT_SECRET_KEY"],  # same as app.config["JWT_SECRET_KEY"]
        algorithms="HS256",  # e.g., ["HS256"]
        options={"verify_exp": False}  # optionally ignore expiry for testing
    )

print(ws_token)

print(decoded)



