import os

# Getting the path of the project root directory and build the SQLite database file location.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

 # secret key is being used for session management with CSRF protection and secure cookies.
 # it will Use Render environment variable in production and fallback value for local development.
class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

# Database connection string
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "smartlocker.db")
    )
# Disables unnecessary SQLAlchemy change tracking
# to improve application performance.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Prevents JavaScript from accessing session cookies,
# helping protect against XSS attacks.
    SESSION_COOKIE_HTTPONLY = True

# Restricts when cookies are sent with requests
# helping reduce Cross-Site Request Forgery (CSRF) attacks.    
    SESSION_COOKIE_SAMESITE = "Lax"

# Ensures cookies are only transmitted over HTTPS
# when running in a production environment.
    SESSION_COOKIE_SECURE = os.getenv(
        "FLASK_ENV"
    ) == "production"