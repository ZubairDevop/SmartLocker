from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    from app.models.user import User


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)

    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    # Import models
    from app.models import (
        User,
        LaptopModel,
        Locker,
        LockerCell,
        Request
    )

    # Register blueprints
    from app.routes import main
    from app.auth import auth
    from app.admin import admin
    from app.user import user

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    return app