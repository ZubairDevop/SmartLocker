from app import db


class LaptopModel(db.Model):
    __tablename__ = "laptop_models"

    id = db.Column(db.Integer, primary_key=True)

    manufacturer = db.Column(db.String(50), nullable=False)

    model = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(20), nullable=False)

    status = db.Column(db.String(20), nullable=False)