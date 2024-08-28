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
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    company_name: Mapped[str] = mapped_column(String(80))
    date_created: Mapped[datetime]
    date_modified: Mapped[datetime]
    sales_contact_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    sales_contact: Mapped["User"] = relationship(back_populates="customers")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="customer")



