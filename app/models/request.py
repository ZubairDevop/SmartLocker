from datetime import datetime
from app import db



class Request(db.Model):
    # Database table name
    __tablename__ = "requests"

     # Unique request identifier
    id = db.Column(db.Integer, primary_key=True)

    # User who submitted the request
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Laptop category requested by the user
    # Standard or Executive
    requested_category = db.Column(
        db.String(20),
        nullable=False
    )

    # Locker cell allocated after approval
    locker_cell_id = db.Column(
        db.Integer,
        db.ForeignKey("locker_cells.id")
    )

    # Description of laptop fault provided by user
    issue_description = db.Column(
        db.Text,
        nullable=False
    )

    # Request priority Low, Medium or High
    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    # Current request status
    # Pending, Ready for Collection, Completed, Rejected, Cancelled
    status = db.Column(
        db.String(30),
        default="Pending"
    )
    # Date request was submitted
    request_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Date request was approved
    approval_date = db.Column(db.DateTime)

    # One-time collection code generated during approval
    collection_code = db.Column(
        db.String(6),
        unique=True
    )

    # Records whether collection code has been viewed
    collection_viewed = db.Column(
        db.Boolean,
        default=False
    )

    # Relationship to requesting user
    user = db.relationship(
        "User",
        back_populates="requests"
    )

    # Relationship to allocated locker cell
    locker_cell = db.relationship("LockerCell")