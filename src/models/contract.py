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
