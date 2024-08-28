from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base


class Team(Base):
    __tablename__ = "team_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    members: Mapped[List["User"]] = relationship(back_populates="team")

    def __str__(self):
        return self.name

    def permissions(self):
        """retourne les permissions de la team"""
        if self.name == "Management team":
            return [
                'create_user',
                'read_user',
                'list_users',
                'delete_users',
                'update_users',
            ]
        if self.name == "Support team":
            return []
        if self.name == "Sales team":
            return []
