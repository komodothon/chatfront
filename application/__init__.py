"""/application/__init__.py"""

from flask import Flask
from extensions import db, bcrypt, jwt, migrate

def create_app(config_class="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)


    print(f"[application/__init__.py]: Before migrate.init_app")
    migrate.init_app(app, db)
    print(f"[application/__init__.py]: After migrate.init_app")

    # Import models BEFORE registering blueprints
    # This ensures models are available when the app context is created
    
    from application.models import User, UserCredential, Message, Room

    # Register blueprints
    from application.routes import all_blueprints
    print(f"[application/__init__.py]: {all_blueprints}")
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint, url_prefix=blueprint.url_prefix)


    return app



