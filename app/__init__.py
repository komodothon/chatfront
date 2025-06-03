"""/app/__init__.py"""

from flask import Flask
from extensions import db, bcrypt, jwt, migrate

def create_app(config_class="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    print("Before migrate.init_app")
    migrate.init_app(app, db)
    print("After migrate.init_app")

    # Import models BEFORE registering blueprints
    # This ensures models are available when the app context is created
    import app.models  # Import models here

    # Register blueprints
    from app.routes import all_blueprints
    print(f"[run.py]: {all_blueprints}")
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=blueprint.url_prefix)


    return app



