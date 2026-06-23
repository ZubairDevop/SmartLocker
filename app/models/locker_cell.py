from app import db

# LockerCell table represents individual cells
# inside the Smart Locker.
class LockerCell(db.Model):
    
    # Database table name
    __tablename__ = "locker_cells"

    # Unique identifier for each locker cell
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking the cell to its locker
    locker_id = db.Column(
        db.Integer,
        db.ForeignKey("lockers.id"),
        nullable=False
    )

    # locker cell number
    cell_number = db.Column(db.Integer, nullable=False)

    laptop_id = db.Column(
        db.Integer,
        db.ForeignKey("laptop_models.id")
    )

    # Current locker cell status
    # Available, Reserved, Repair or Empty
    status = db.Column(
        db.String(20),
        default="Available"
    )

    # Relationship to parent locker
    locker = db.relationship("Locker")

    # Relationship to laptop stored in cell
    laptop = db.relationship("LaptopModel")