from datetime import datetime
from app import db


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    requested_category = db.Column(
        db.String(20),
        nullable=False
    )

    locker_cell_id = db.Column(
        db.Integer,
        db.ForeignKey("locker_cells.id")
    )

    issue_description = db.Column(
        db.Text,
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    status = db.Column(
        db.String(30),
        default="Pending"
    )

    request_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    approval_date = db.Column(db.DateTime)

    collection_code = db.Column(
        db.String(6),
        unique=True
    )

    collection_viewed = db.Column(
        db.Boolean,
        default=False
    )

    user = db.relationship(
        "User",
        back_populates="requests"
    )

    locker_cell = db.relationship("LockerCell")