from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base


class User(Base):

    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    personal_number: Mapped[str] = mapped_column(String(10), unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    team_id: Mapped[int] = mapped_column(ForeignKey("team_table.id"))
    team: Mapped["Team"] = relationship(back_populates="members")
    customers: Mapped[List["Customer"]] = relationship("Customer", back_populates="sales_contact")
    managed_events: Mapped[List["Event"]] = relationship("Event", back_populates="support_contact")

    @property
    def has_perm(self, permission: str) -> bool:
        """retourne True si permission fait partie des permissions de son équipe"""
        return permission in self.team.permissions()










