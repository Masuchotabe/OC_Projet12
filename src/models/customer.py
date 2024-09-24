from __future__ import annotations

import enum
import re
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, String, select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base
from .user import User


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    company_name: Mapped[str] = mapped_column(String(80))
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)
    date_modified: Mapped[datetime] = mapped_column(default=datetime.now, onupdate=datetime.now)
    sales_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    sales_contact: Mapped["User"] = relationship(back_populates="customers")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="customer")

    @classmethod
    def validate_email(cls, email):
        """Validate email"""
        if email and not re.match(r"^((?!\.)[\w\-_.+]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", email):
            raise ValueError("""The email is not valid.""")
        return email

    @classmethod
    def validate_data(cls, customer_data):
        """
        Validate some customer data.
        Args :
            customer_data(dict): dict of customer datas
        Returns[str]: list of errors
        """
        errors = []
        for field_name, value in customer_data.items():
            if hasattr(cls, 'validate_' + field_name):
                try:
                    getattr(cls, 'validate_' + field_name)(value)
                except ValueError as e:
                    errors.append(str(e))
        return errors

    @classmethod
    def get_customers(cls, session):
        """Retourne une liste des clients"""
        return session.scalars(select(cls)).all()

    @classmethod
    def get_customer(cls, session, email):
        """Retourne un client à partir de son email"""
        return session.scalar(select(cls).where(cls.email == email))

    @classmethod
    def create(cls, session, customer_data):
        """
        Crée un client et le retourne
        Args:
            session(sqlalchemy.orm.Session): session
            customer_data(dict): dict of client datas

        Returns(User):

        """
        customer = cls()
        customer._update_data(customer_data)

        session.add(customer)
        session.commit()
        return customer

    def update(self, session, customer_data):
        """
        Met à jour un utilisateur
        Args :
            session (Session) : session
            customer_data (dict) : dict of client datas
        """
        self._update_data(customer_data)
        session.commit()


    def _update_data(self, customer_data):
        """Met à jour les données du client"""
        for key, value in customer_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

