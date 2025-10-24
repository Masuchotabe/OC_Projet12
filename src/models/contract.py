from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from sentry_sdk import capture_message
from sqlalchemy import Enum, String, select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from . import Base
from .user import User


class ContractStatus(enum.Enum):
    """Enum representing possible statuses of a contract."""
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
        """
        Validate the status value.
        Args:
            value(str): The status to validate.
        Returns:
            str: Validated status value.
        """
        # if value not in ContractStatus.
        if value not in [status.value for status in ContractStatus]:
            raise ValueError('Status not in choice')
        return value

    @classmethod
    def validate_data(cls, contract_data):
        """
        Validate contract data.

        Args:
            contract_data(dict): Dictionary containing contract data.

        Returns:
            list: A list of validation errors, empty if the data is valid.
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
        """
        Retrieve a list of contracts based on filters.
        Args:
            session(Session): SQLAlchemy session.
            not_signed(bool): If True, filter only contracts with status 'Created'.
            unpaid_contracts(bool): If True, filter contracts with remaining balance greater than zero.
        Returns:
            List[Contract]: List of filtered contracts.
        """
        query = select(cls)
        if not_signed:
            query = query.where(cls.status == ContractStatus.CREATED)
        elif unpaid_contracts:
            query = query.where(cls.remaining_balance > 0)
        return session.scalars(query).all()

    @classmethod
    def get_contract(cls, session, id):
        """
        Retrieve a specific contract by its ID.
        Args:
            session(Session): SQLAlchemy session.
            id(int): ID of the contract.
        Returns:
            Optional[Contract]: The contract if found, otherwise None.
        """
        return session.scalar(select(cls).where(cls.id == id))

    @classmethod
    def create(cls, session, contract_data):
        """
        Create and return a new contract.
        Args:
            session(Session): SQLAlchemy session.
            contract_data(dict): Dictionary containing contract data.
        Returns:
            Contract: The newly created contract.
        """
        contract = cls()
        contract._update_data(contract_data)

        session.add(contract)
        session.commit()
        return contract

    def update(self, session, contract_data):
        """
        Update an existing contract with new data.
        Args:
            session(Session): SQLAlchemy session.
            contract_data(dict): Dictionary containing updated contract data.
        """
        self._update_data(contract_data)
        session.commit()

    def _update_data(self, customer_data):
        """
        Internal method to update contract data.
        Args:
            contract_data(dict): Dictionary containing data to update.
        """
        for key, value in customer_data.items():
            if key == 'status' and value == ContractStatus.SIGNED.value and self.status == ContractStatus.CREATED:
                capture_message('New contract signed')
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self, session):
        """
        Delete the current contract.
        Args:
            session(Session): SQLAlchemy session.
        """
        session.delete(self)
        session.commit()
