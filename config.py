"""/config.py"""

import os
from datetime import timedelta

from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "app_secret_key")    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 12
    SESSION_COOKIE_SECURE = False

    # JWT related
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    print(f"[config.py] JWT_SECRET_KEY: {JWT_SECRET_KEY}")
    
    JWT_TOKEN_LOCATION = os.getenv("JWT_TOKEN_LOCATION", "cookies").split(",")
    JWT_ACCESS_COOKIE_PATH = os.getenv("JWT_ACCESS_COOKIE_PATH", "/")
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "False").lower() in ("true", "1", "yes")
    JWT_COOKIE_CSRF_PROTECT = os.getenv("JWT_COOKIE_CSRF_PROTECT", "True").lower() in ("true", "1", "yes")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)))


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URI",
        "postgresql://chatuser:chatpassword@140.245.232.106:5432/chatapp_dev"
    )

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        "postgresql://chatuser:chatpassword@140.245.232.106:5432/chatapp_dev"
    )
    BCRYPT_LOG_ROUNDS = 4  # Faster hashing for tests


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "postgresql://chatuser:chatpassword@140.245.232.106:5432/chatapp_dev"
    )
    SESSION_COOKIE_SECURE = True  # Required for HTTPS
