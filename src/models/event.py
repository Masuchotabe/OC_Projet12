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
        """
        Validate the event start date format.
        Args:
            value (str): The start date of the event in 'YYYY-MM-DD HH:MM' format.
        Returns:
            datetime: The validated start date as a datetime object.
        """
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("""The date should respect YYYY-MM-DD HH:MM format.""")

    @classmethod
    def validate_event_end_date(cls, value):
        """
        Validate the event end date format.
        Args:
            value (str): The end date of the event in 'YYYY-MM-DD HH:MM' format.
        Returns:
            datetime: The validated end date as a datetime object.
        """
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        except ValueError:
            raise ValueError("""The date should respect YYYY-MM-DD HH:MM format.""")

    @classmethod
    def validate_data(cls, event_data):
        """
        Validate the event data.

        Args:
            event_data (dict): A dictionary containing the event data.

        Returns:
            List[str]: A list of validation error messages, empty if no errors.
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
    def get_events(cls, session, user=None, filter_empty=False, user_only=False):
        """
        Retrieve a list of events.
        Args:
            session (Session): SQLAlchemy session.
            user (User, optional): The user to filter events by. Defaults to None.
            filter_empty (bool, optional): Flag to filter events without support contact. Defaults to False.
            user_only (bool, optional): Flag to filter events assigned to the user. Defaults to False.
        Returns:
            List[Event]: A list of events that match the filtering criteria.
        """
        query = select(cls)
        if user and user_only:
            query = query.filter(cls.support_contact == user)
        elif filter_empty:
            query = query.filter(cls.support_contact_id == None)
        return session.scalars(query).all()

    @classmethod
    def get_event(cls, session, id):
        """
        Retrieve an event by its ID.
        Args:
            session (Session): SQLAlchemy session.
            id (int): The ID of the event to retrieve.
        Returns:
            Event or None: The event with the given ID, or None if not found.
        """
        return session.scalar(select(cls).where(cls.id == id))

    @classmethod
    def create(cls, session, event_data):
        """
        Create a new event and return it.
        Args:
            session (Session): SQLAlchemy session.
            event_data (dict): A dictionary containing the event data.
        Returns:
            Event: The newly created event.
        """
        event = cls()
        event._update_data(event_data)

        session.add(event)
        session.commit()
        return event

    def update(self, session, event_data):
        """
        Update an existing event.
        Args:
            session (Session): SQLAlchemy session.
            event_data (dict): A dictionary containing the updated event data.
        """
        self._update_data(event_data)
        session.commit()

    def _update_data(self, event_data):
        """
        Internal method to update the event data.

        Args:
            event_data (dict): A dictionary containing the event data to update.
        """
        for key, value in event_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self, session):
        """
        Delete the event from the database.
        Args:
            session (Session): SQLAlchemy session.
        """
        session.delete(self)
        session.commit()

