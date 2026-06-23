from app import db

# LaptopModel table stores all laptop models available
# for replacement requests and locker allocation.
class LaptopModel(db.Model):
    __tablename__ = "laptop_models"

    # Unique identifier for each laptop model
    id = db.Column(db.Integer, primary_key=True)

    # Laptop manufacturer (Dell, Lenovo, Fujitsu, Apple, Microsoft)
    manufacturer = db.Column(db.String(50), nullable=False)

    # Specific laptop model
    model = db.Column(db.String(100), nullable=False)

    # Laptop category (Standard or Executive)
    category = db.Column(db.String(20), nullable=False)

    # Current laptop status
    # Available, Repair or Retired
    status = db.Column(db.String(20), nullable=False)