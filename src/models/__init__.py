from sqlalchemy.orm import DeclarativeBase


# app/models/__init__.py

class Base(DeclarativeBase):
    pass


from .user import User
from .team import Team
from .customer import Customer, Contract, Event




