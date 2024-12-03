from __future__ import annotations

import re
from typing import List, Optional
from passlib.hash import argon2
from sentry_sdk import capture_message
from sqlalchemy import ForeignKey, String, select
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

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    @classmethod
    def validate_username(cls, username):
        """
        Validate the username format.
        Args:
            username (str): The username to validate.
        Returns:
            str: The validated username.
        """
        if len(username) < 5 or not re.match(r"^[a-zA-Z][a-zA-Z0-9]+$", username):
            raise ValueError("""The username must contain at least 5 characters and consist only of letters and number, starting with a letter.""")
        return username

    @classmethod
    def validate_email(cls, email):
        """
        Validate the email format.
        Args:
            email (str): The email address to validate.
        Returns:
            str: The validated email.
        """
        if email and  not re.match(r"^((?!\.)[\w\-_.+]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", email):
            raise ValueError("""The email is not valid.""")
        return email

    @classmethod
    def validate_personal_number(cls, personal_number):
        """
        Validate the employee personal number (ID).
        Args:
            personal_number (str): The employee number to validate.
        Returns:
            str: The validated personal number.
        """
        if len(personal_number) != 10 or not re.match(r"^[0-9]+$", personal_number):
            raise ValueError("""Employee ID must be 10 numbers""")
        return personal_number

    @classmethod
    def validate_password(cls, password):
        """
        Validate the password format.
        Args:
            password (str): The password to validate.
        Returns:
            str: The validated password.
        """
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password):
            raise ValueError("""Password must contain at least 8 characters, including lowercase, uppercase, and a number.""")
        return password

    @classmethod
    def validate_data(cls, user_data):
        """
        Validate the user data fields.
        Args:
            user_data (dict): A dictionary containing user data to validate.
        Returns:
            List[str]: A list of validation error messages. Empty if no errors.
        """
        errors = []
        for field_name, value in user_data.items():
            if hasattr(cls, 'validate_'+field_name):
                try:
                    getattr(cls, 'validate_'+field_name)(value)
                except ValueError as e:
                    errors.append(str(e))
        return errors

    @classmethod
    def get_users(cls, session):
        """
        Retrieve a list of all users.
        Args:
            session (Session): SQLAlchemy session.
        Returns:
            List[User]: A list of all users.
        """
        return session.scalars(select(cls)).all()

    @classmethod
    def get_user(cls, session, username):
        """
        Retrieve a user by their username.
        Args:
            session (Session): SQLAlchemy session.
            username (str): The username of the user to retrieve.
        Returns:
            Optional[User]: The user with the given username, or None if not found.
        """
        return session.scalar(select(cls).where(cls.username == username))

    @classmethod
    def create(cls, session, user_data):
        """
        Create a new user and return it.
        Args:
            session (Session): SQLAlchemy session.
            user_data (dict): A dictionary containing user data.
        Returns:
            User: The newly created user.
        """
        user_data['password'] = argon2.hash(user_data['password'])
        user = cls()
        user._update_data(user_data)

        session.add(user)
        session.commit()
        capture_message(f"User created : {user.username}")
        return user

    def update(self, session, user_data):
        """
        Update an existing user.
        Args:
            session (Session): SQLAlchemy session.
            user_data (dict): A dictionary containing updated user data.
        """
        if user_data.get('password'):
            user_data['password'] = argon2.hash(user_data['password'])
        self._update_data(user_data)
        capture_message(f"User updated : {self.username}")
        session.commit()


    def _update_data(self, user_data):
        """
        Internal method to update the user data fields.
        Args:
            user_data (dict): A dictionary containing user data to update.
        """
        for key, value in user_data.items():
            if hasattr(self, key):
                setattr(self, key, value)


    def delete(self, session):
        """
        Delete the user from the database.
        Args:
            session (Session): SQLAlchemy session.
        """
        session.delete(self)
        session.commit()

    def has_perm(self, permission: str) -> bool:
        """
        Check if the user has a specific permission.
        Args:
            permission (str): The permission to check.
        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return permission in self.team.permissions()
