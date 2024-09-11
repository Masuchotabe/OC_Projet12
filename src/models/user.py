from __future__ import annotations

import re
from typing import List, Optional
from passlib.hash import argon2
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

    @classmethod
    def validate_data(cls, user_data):
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

    @classmethod
    def get_users(cls, session):
        """Retourne une liste des équipes"""
        return session.scalars(select(cls)).all()

    @classmethod
    def get_user(cls, session, username):
        """Retourne une équipe à partir de son username"""
        return session.scalar(select(cls).where(cls.username == username))

    @classmethod
    def create(cls, session, user_data):
        """
        Crée un user et le retourne
        Args:
            session(sqlalchemy.orm.Session): session
            user_data(dict): dict of user datas

        Returns:

        """
        user_data['password'] = argon2.hash(user_data['password'])
        user = cls()
        user._update_data(user_data)

        session.add(user)
        session.commit()
        return user

    def update(self, session, user_data):
        """
        Met à jour un utilisateur
        Args:
            session(session): session de db
            user_data: Données utilisateur
        """
        if user_data['password']:
            user_data['password'] = argon2.hash(user_data['password'])
        self._update_data(user_data)
        session.commit()


    def _update_data(self, user_data):
        """Met à jour les données utilisateur"""
        for key, value in user_data.items():
            if hasattr(self, key):
                setattr(self, key, value)


    def delete(self, session):
        """Supprimer l'utilisateur"""
        session.delete(self)
        session.commit()

    def has_perm(self, permission: str) -> bool:
        """retourne True si permission fait partie des permissions de son équipe"""
        return permission in self.team.permissions()
