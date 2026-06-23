from app import db


class Locker(db.Model):
     # Database table name
    __tablename__ = "lockers"

    # Unique identifier for each locker
    id = db.Column(db.Integer, primary_key=True)

    # Locker name (Smart Locker)
    locker_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )