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
