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


class ContractStatus(enum.Enum):
    CREATED = 'Created'
    SIGNED = 'Signed'
    FINISHED = 'Finished'


class Contract(Base):
    __tablename__ = "contract_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    total_balance: Mapped[float]
    remaining_balance: Mapped[float]
    status: Mapped[ContractStatus]
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer: Mapped["Customer"] = relationship(back_populates="contracts")
    events: Mapped[List["Event"]] = relationship(back_populates="contract")

    @classmethod
    def validate_status(cls, value):
        """Assert status is in the choice"""
        # if value not in ContractStatus.
        if value not in [status.value for status in ContractStatus]:
            raise ValueError('Status not in choice')
        return value

    @classmethod
    def validate_data(cls, contract_data):
        """
        Valide les données d'un contrat

        Args:
            contract_data (dict): Dictionnaire contenant les données du contrat

        Returns:
            list: Une liste d'erreurs de validation, vide si les données sont valides
        """
        errors = []

        for field_name, value in contract_data.items():
            if hasattr(cls, 'validate_' + field_name):
                try:
                    contract_data[field_name] = getattr(cls, 'validate_' + field_name)(value)
                except ValueError as e:
                    errors.append(str(e))
        if 'total_balance' in contract_data and 'remaining_balance' in contract_data:
            if contract_data['remaining_balance'] > contract_data['total_balance']:
                errors.append("Remaining balance can't be greater than total balance.")

        return errors

    @classmethod
    def get_contracts(cls, session, not_signed, unpaid_contracts):
        """Retourne une liste de tous les contrats"""
        query = select(cls)
        if not_signed:
            query = query.where(cls.status == ContractStatus.CREATED)
        elif unpaid_contracts:
            query = query.where(cls.remaining_balance > 0)
        return session.scalars(query).all()

    @classmethod
    def get_contract(cls, session, id):
        """Retourne un contrat à partir de son ID"""
        return session.scalar(select(cls).where(cls.id == id))

    @classmethod
    def create(cls, session, contract_data):
        """Crée un contrat et le retourne"""
        contract = cls()
        contract._update_data(contract_data)

        session.add(contract)
        session.commit()
        return contract

    def update(self, session, contract_data):
        """Met à jour un contrat"""
        self._update_data(contract_data)
        session.commit()

    def _update_data(self, customer_data):
        """Met à jour les données du client"""
        for key, value in customer_data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self, session):
        """Supprime le contrat"""
        session.delete(self)
        session.commit()
