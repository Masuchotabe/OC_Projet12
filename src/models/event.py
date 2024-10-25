from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, String, select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base
from .user import User


class Event(Base):
    __tablename__ = "event_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_start_date: Mapped[datetime]
    event_end_date: Mapped[datetime]
    location: Mapped[str] = mapped_column(String(250))
    attendees: Mapped[int]
    notes: Mapped[Optional[str]] = mapped_column(String(1000))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract_table.id"))
    contract: Mapped["Contract"] = relationship(back_populates="events")
    support_contact_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user_table.id"))
    support_contact: Mapped[Optional["User"]] = relationship(back_populates="managed_events")

    @classmethod
    def validate_event_start_date(cls, value):
        """validate event start date"""
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("""The date should respect YYYY-MM-DD HH:MM format.""")

    @classmethod
    def validate_event_end_date(cls, value):
        """validate event start date"""
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("""The date should respect YYYY-MM-DD HH:MM format.""")

    @classmethod
    def validate_data(cls, event_data):
        """
        Valide les données d'un événement.

        Args:
            event_data (dict): Dictionnaire contenant les données de l'événement.

        Returns:
            list: Une liste d'erreurs de validation.
        """
        errors = []

        for field_name, value in event_data.items():
            if hasattr(cls, 'validate_' + field_name):
                try:
                    event_data[field_name] = getattr(cls, 'validate_' + field_name)(value)
                except ValueError as e:
                    errors.append(str(e))
        if event_data['event_start_date'] and event_data['event_end_date']:
            if event_data['event_start_date'] > event_data['event_end_date']:
                errors.append('Event end date must be after event start date.')

        return errors

    @classmethod
    def get_events(cls, session):
        """Retourne une liste de tous les événements"""
        return session.scalars(select(cls)).all()

    @classmethod
    def get_event(cls, session, id):
        """Retourne un événement à partir de son ID"""
        return session.scalar(select(cls).where(cls.id == id))

    @classmethod
    def create(cls, session, event_data):
        """Crée un événement et le retourne"""
        event = cls()
        event._update_data(event_data)

        session.add(event)
        session.commit()
        return event

    def update(self, session, event_data):
        """
        Met à jour un évènement
        Args :
            session (Session) : session
            event_data (dict) : dict of event datas
        """
        self._update_data(event_data)
        session.commit()

    def _update_data(self, event_data):
        """Met à jour les données du client"""
        for key, value in event_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self, session):
        """Supprime l'événement"""
        session.delete(self)
        session.commit()

