"""/application/routes/__init__.py"""

from flask import Blueprint

from application.routes.main import main_bp
from application.routes.auth import auth_bp

all_blueprints = []

all_blueprints.append(main_bp)
all_blueprints.append(auth_bp)

