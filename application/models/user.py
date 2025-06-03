"""application/models/user.py"""

from extensions import db, bcrypt
from application.models.base import BaseModel
from application.models.message import Message


class User(BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    # One-to-one relationship with credentials
    credential = db.relationship(
        "UserCredential",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Messages sent by this user
    sent_messages = db.relationship(
        "Message",
        back_populates="sender",
        foreign_keys=[Message.sender_id],
        uselist=True
    )

    # Messages received by this user (DMs)
    received_messages = db.relationship(
        "Message",
        back_populates="receiver",
        foreign_keys=[Message.receiver_id],
        uselist=True
    )

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def set_password(self, plain_password):
        password_hash = bcrypt.generate_password_hash(plain_password).decode('utf-8')
        self.credential = UserCredential(password_hash=password_hash)

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.credential.password_hash, plain_password)

    def to_safe_dict(self):
        return {
            "id": self.id,
            "username": self.username
        }


class UserCredential(BaseModel):
    __tablename__ = 'user_credentials'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

    # back-reference
    user = db.relationship("User", back_populates="credential")
