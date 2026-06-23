# Import Flask framework and extensions used by the application.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Create shared extension objects.
# These are initialised later inside create_app()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# this function creates and configures a new Flask application instance. and importing user model for flask login
def create_app():
    from app.models.user import User


    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app = Flask(__name__)

    # Load application configuration from config.py.
    app.config.from_object("config.Config")

    # Initialise SQLAlchemy database connection.
    db.init_app(app)

    # Initialise authentication and CSRF protection.
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configuring login behaviour.if users attempting to access protected pages are redirected to login.
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

    
    from app.routes import main
    from app.auth import auth
    from app.admin import admin
    from app.user import user

# Register blueprints. Each blueprint contains a separate area of functionality.
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    return app