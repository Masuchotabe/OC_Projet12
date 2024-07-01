from __future__ import annotations

from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base
from .user import User


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[Optional[str]]
    company_name: Mapped[str]
    date_created: Mapped[datetime]
    date_modified: Mapped[datetime]
    sales_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    sales_contact: Mapped["User"] = relationship(back_populates="customers")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="customer")

import enum
from sqlalchemy import Enum


class ContractStatus(enum.Enum):
    NOT_STARTED = 'Non commencé'
    IN_PROGRESS = 'En cours'
    FINISHED = 'Terminé'


class Contract(Base):
    __tablename__ = "contract_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_balance: Mapped[float]
    remaining_balance: Mapped[float]
    status: Mapped[Enum[ContractStatus]]
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contracts")
    events: Mapped[List["Event"]] = relationship(back_populates="contract")


class Event(Base):
    __tablename__ = "event_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_start_date: Mapped[datetime]
    event_end_date: Mapped[datetime]
    location: Mapped[str]
    attendees: Mapped[int]
    notes: Mapped[str]
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract_table.id"))
    contract: Mapped["Contract"] = relationship(back_populates="events")
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    support_contact: Mapped["User"] = relationship(back_populates="managed_events")




