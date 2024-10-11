from __future__ import annotations
from typing import List, Optional

from sqlalchemy import ForeignKey, String, event, insert, select
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
        base_perms = [
            'list_contracts',
            'read_contract',
            'list_events',
            'read_event',
            'list_customers',
            'read_customer',
        ]
        if self.name == "Management team":
            return base_perms + [
                'create_user',
                'read_user',
                'list_users',
                'delete_user',
                'update_user',
                'create_contract',
                'update_contract',
                'update_event',
            ]
        if self.name == "Sales team":
            return base_perms + [
                'create_customer',
                'update_customer',
                'update_contract',
                'create_event',
            ]
        if self.name == "Support team":
            return base_perms + [
                'update_event',
            ]


    @classmethod
    def get_teams(cls, session):
        """Retourne une liste des équipes"""
        return session.scalars(select(cls)).all()

    @classmethod
    def get_team(cls, session, team_name):
        """Retourne une équipe à partir de son nom"""
        return session.scalar(select(cls).where(cls.name==team_name))

@event.listens_for(Team.__table__, "after_create")
def init_team(target, connection, **kwargs):
    """listen for the 'after_create' event --> only if we use metadata.create_all"""
    connection.execute(insert(target).values(name="Management team"))
    connection.execute(insert(target).values(name="Sales team"))
    connection.execute(insert(target).values(name="Support team"))
