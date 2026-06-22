from app import db


class LockerCell(db.Model):
    __tablename__ = "locker_cells"

    id = db.Column(db.Integer, primary_key=True)

    locker_id = db.Column(
        db.Integer,
        db.ForeignKey("lockers.id"),
        nullable=False
    )

    cell_number = db.Column(db.Integer, nullable=False)

    laptop_id = db.Column(
        db.Integer,
        db.ForeignKey("laptop_models.id")
    )

    status = db.Column(
        db.String(20),
        default="Available"
    )

    locker = db.relationship("Locker")

    laptop = db.relationship("LaptopModel")