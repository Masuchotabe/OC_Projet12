from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base
from .customer import Customer, Event


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    password: Mapped[str]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    team_id: Mapped[int] = mapped_column(ForeignKey("team_table.id"))
    team: Mapped["Team"] = relationship(back_populates="members")
    customers: Mapped[List["Customer"]] = relationship(back_populates="sales_contact")
    managed_events: Mapped[List["Event"]] = relationship(back_populates="support_contact")


class Team(Base):
    __tablename__ = "team_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    members: Mapped[List["User"]] = relationship(back_populates="team")






