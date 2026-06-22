from app import db


class Locker(db.Model):
    __tablename__ = "lockers"

    id = db.Column(db.Integer, primary_key=True)

    locker_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True
    )