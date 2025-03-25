import pytest
from sqlalchemy import select, func
from datetime import datetime
import re

from models import Customer, User



def test_customer_str(customer):
    """Test the __str__ method of Customer"""
    assert str(customer) == "Test Customer"


def test_validate_email_valid():
    """Test validate_email with valid email"""
    valid_email = "test@example.com"
    assert Customer.validate_email(valid_email) == valid_email


def test_validate_email_invalid():
    """Test validate_email with invalid email"""
    invalid_email = "invalid-email"
    with pytest.raises(ValueError):
        Customer.validate_email(invalid_email)


def test_validate_data_valid(customer_data):
    """Test validate_data with valid data"""
    errors = Customer.validate_data(customer_data)
    assert len(errors) == 0


def test_validate_data_invalid():
    """Test validate_data with invalid data"""
    invalid_data = {"email": "invalid-email"}
    errors = Customer.validate_data(invalid_data)
    assert len(errors) > 0


def test_get_customers(session, customer):
    """Test get_customers method"""
    customers = Customer.get_customers(session)
    assert len(customers) >= 1
    assert customer in customers


def test_get_customer(session, customer):
    """Test get_customer method"""
    found_customer = Customer.get_customer(session, customer.email)
    assert found_customer is not None
    assert found_customer.id == customer.id


def test_get_customer_not_found(session):
    """Test get_customer method with non-existent email"""
    non_existent_email = "nonexistent@example.com"
    customer = Customer.get_customer(session, non_existent_email)
    assert customer is None


def test_create_customer(session, customer_data):
    """Test create method"""
    customer = Customer.create(session, customer_data)
    assert customer is not None
    assert customer.name == customer_data["name"]
    assert customer.email == customer_data["email"]
    assert customer.phone == customer_data["phone"]
    assert customer.company_name == customer_data["company_name"]
    assert customer.sales_contact_id == customer_data["sales_contact_id"]
    assert customer.date_created is not None
    assert customer.date_modified is not None

    # Clean up
    session.delete(customer)
    session.commit()


def test_update_customer(session, customer):
    """Test update method"""
    updated_data = {
        "name": "Updated Customer",
        "phone": "9876543210"
    }

    customer.update(session, updated_data)

    # Refresh the customer from the database
    session.refresh(customer)

    assert customer.name == updated_data["name"]
    assert customer.phone == updated_data["phone"]
    # Other fields should remain unchanged
    assert customer.email == "test@example.com"
    assert customer.company_name == "Test Company"


def test_update_data_internal(customer):
    """Test _update_data internal method"""
    updated_data = {
        "name": "Internal Update",
        "email": "internal@example.com"
    }

    customer._update_data(updated_data)

    assert customer.name == updated_data["name"]
    assert customer.email == updated_data["email"]
