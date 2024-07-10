from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, String
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
    email: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    company_name: Mapped[str] = mapped_column(String(80))
    date_created: Mapped[datetime]
    date_modified: Mapped[datetime]
    sales_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    sales_contact: Mapped["User"] = relationship(back_populates="customers")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="customer")


class ContractStatus(enum.Enum):
    CREATED = 'Non commencé'
    SIGNED = 'En cours'
    FINISHED = 'Terminé'


class Contract(Base):
    __tablename__ = "contract_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_balance: Mapped[float]
    remaining_balance: Mapped[float]
    status: Mapped[ContractStatus]
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contracts")
    events: Mapped[List["Event"]] = relationship(back_populates="contract")


class Event(Base):
    __tablename__ = "event_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_start_date: Mapped[datetime]
    event_end_date: Mapped[datetime]
    location: Mapped[str] = mapped_column(String(250))
    attendees: Mapped[int]
    notes: Mapped[str] = mapped_column(String(1000))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract_table.id"))
    contract: Mapped["Contract"] = relationship(back_populates="events")
    support_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    support_contact: Mapped["User"] = relationship(back_populates="managed_events")
