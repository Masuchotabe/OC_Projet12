from __future__ import annotations

import re
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, validates
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

    @classmethod
    def validate_username(cls, username):
        """Validate username"""
        if len(username) < 5 or not re.match(r"^[a-zA-Z][a-zA-Z0-9]+$", username):
            raise ValueError("""The username must contain at least 5 characters and consist only of letters and number, starting with a letter.""")
        return username

    @classmethod
    def validate_email(cls, email):
        """Validate email"""
        if email and  not re.match(r"^((?!\.)[\w\-_.+]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", email):
            raise ValueError("""The email is not valid.""")
        return email

    @classmethod
    def validate_personal_number(cls, personal_number):
        """Validate email"""
        if len(personal_number) != 10 or not re.match(r"^[0-9]+$", personal_number):
            raise ValueError("""Employee ID must be 10 numbers""")
        return personal_number

    @classmethod
    def validate_password(cls, password):
        """Validate email"""
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password):
            raise ValueError("""Password must contain at least 8 characters, including lowercase, uppercase, and a number.""")
        return password

    def has_perm(self, permission: str) -> bool:
        """retourne True si permission fait partie des permissions de son équipe"""
        return permission in self.team.permissions()

    @classmethod
    def validate_user_data(cls, user_data):
        """
        Validate some user data.
        :param user_data(dict): dict of user datas
        :return: list of errors
        """
        errors = []
        for field_name, value in user_data.items():
            if hasattr(cls, 'validate_'+field_name):
                try:
                    getattr(cls, 'validate_'+field_name)(value)
                except ValueError as e:
                    errors.append(str(e))
        return errors










