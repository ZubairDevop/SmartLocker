# Flask-Login mixin provides authentication features
from flask_login import UserMixin
from app import db
from datetime import datetime

# Password hashing functions
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# User table stores all employees and administrators
# who access the Smart Locker system.
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    department = db.Column(db.String(100), nullable=False)

    job_title = db.Column(db.String(100), nullable=False)

    # Laptop entitlement category
    # Standard or Executive
    assigned_category = db.Column(db.String(20), nullable=False)

    # User role
    # Admin or User
    role = db.Column(db.String(20), nullable=False)

    # Stores encrypted password
    password_hash = db.Column(db.String(255), nullable=False)

    # Laptop currently assigned to user
    current_laptop_id = db.Column(
        db.Integer,
        db.ForeignKey("laptop_models.id")
    )

    # Relationship to assigned laptop
    current_laptop = db.relationship(
        "LaptopModel",
        foreign_keys=[current_laptop_id]
    )

    # Relationship to replacement requests
    requests = db.relationship(
        "Request",
        back_populates="user",
        lazy=True
    )

    # Records when user record was last modified
    updated_at = db.Column(
    db.DateTime,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)

     # Encrypt and store password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify entered password against stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)