from sqlalchemy.orm import DeclarativeBase


# app/models/__init__.py

class Base(DeclarativeBase):
    pass


from .user import User, Team
from .customer import Customer, Contract, Event




