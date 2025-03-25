import pytest
from sqlalchemy import select, func
from datetime import datetime

from models import Contract, ContractStatus, Customer, User


def test_validate_status_valid():
    """Test validate_status with valid status"""
    valid_status = ContractStatus.CREATED.value
    assert Contract.validate_status(valid_status) == valid_status


def test_validate_status_invalid():
    """Test validate_status with invalid status"""
    invalid_status = "Invalid Status"
    with pytest.raises(ValueError):
        Contract.validate_status(invalid_status)


def test_validate_data_valid(contract_data_for_validation):
    """Test validate_data with valid data"""
    errors = Contract.validate_data(contract_data_for_validation)
    assert len(errors) == 0


def test_validate_data_invalid_status():
    """Test validate_data with invalid status"""
    invalid_data = {"status": "Invalid Status"}
    errors = Contract.validate_data(invalid_data)
    assert len(errors) > 0


def test_validate_data_invalid_balance():
    """Test validate_data with remaining_balance > total_balance"""
    invalid_data = {
        "total_balance": 500.0,
        "remaining_balance": 1000.0
    }
    errors = Contract.validate_data(invalid_data)
    assert len(errors) > 0
    assert "Remaining balance can't be greater than total balance." in errors


def test_get_contracts(session, contract):
    """Test get_contracts method"""
    contracts = Contract.get_contracts(session, not_signed=False, unpaid_contracts=False)
    assert len(contracts) >= 1
    assert contract in contracts


def test_get_contracts_not_signed(session, contract):
    """Test get_contracts method with not_signed=True"""
    contracts = Contract.get_contracts(session, not_signed=True, unpaid_contracts=False)
    assert len(contracts) >= 1
    assert contract in contracts  # Our test contract has status CREATED


def test_get_contracts_unpaid(session, contract):
    """Test get_contracts method with unpaid_contracts=True"""
    contracts = Contract.get_contracts(session, not_signed=False, unpaid_contracts=True)
    assert len(contracts) >= 1
    assert contract in contracts  # Our test contract has remaining_balance > 0


def test_get_contract(session, contract):
    """Test get_contract method"""
    found_contract = Contract.get_contract(session, contract.id)
    assert found_contract is not None
    assert found_contract.id == contract.id


def test_get_contract_not_found(session):
    """Test get_contract method with non-existent id"""
    non_existent_id = 9999
    contract = Contract.get_contract(session, non_existent_id)
    assert contract is None


def test_create_contract(session, contract_data):
    """Test create method"""
    contract = Contract.create(session, contract_data)
    assert contract is not None
    assert contract.total_balance == contract_data["total_balance"]
    assert contract.remaining_balance == contract_data["remaining_balance"]
    assert contract.status == contract_data["status"]
    assert contract.customer_id == contract_data["customer_id"]

    # Clean up
    session.delete(contract)
    session.commit()


def test_update_contract(session, contract):
    """Test update method"""
    updated_data = {
        "total_balance": 2000.0,
        "remaining_balance": 1000.0,
        "status": ContractStatus.SIGNED
    }

    contract.update(session, updated_data)

    # Refresh the contract from the database
    session.refresh(contract)

    assert contract.total_balance == updated_data["total_balance"]
    assert contract.remaining_balance == updated_data["remaining_balance"]
    assert contract.status == updated_data["status"]


def test_update_data_internal(contract):
    """Test _update_data internal method"""
    updated_data = {
        "total_balance": 3000.0,
        "status": ContractStatus.FINISHED
    }

    contract._update_data(updated_data)

    assert contract.total_balance == updated_data["total_balance"]
    assert contract.status == updated_data["status"]
    # remaining_balance should be unchanged
    assert contract.remaining_balance == 500.0


def test_delete_contract(session, contract_data):
    """Test delete method"""
    contract = Contract.create(session, contract_data)
    contract_id = contract.id

    # Verify contract exists
    assert Contract.get_contract(session, contract_id) is not None

    # Delete contract
    contract.delete(session)

    # Verify contract no longer exists
    assert Contract.get_contract(session, contract_id) is None
