from app import db

# Import all database models used by the Smart Locker application.
# These imports register the tables with SQLAlchemy.
from .user import User
from .laptop_model import LaptopModel
from .locker import Locker
from .locker_cell import LockerCell
from .request import Request