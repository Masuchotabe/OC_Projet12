from datetime import datetime, timezone, timedelta

import jwt
import pytest
from passlib.handlers.argon2 import argon2
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import User, Customer, Contract, ContractStatus, Event
from settings import SECRET_KEY
from models import Base, Team


@pytest.fixture(scope='session')
def engine():
    """
    Create engine with sql lite db
    :return(e
    """
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    # Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(engine):
    TestingSession = sessionmaker(bind=engine)
    session = TestingSession()
    yield session
    session.close()

@pytest.fixture(scope='function')
def user(session):
    user_data = {
        'username': 'test_admin',
        'password': argon2.hash('test_password'),
        'personal_number': '0000000000',
        'email': 'admin@email.com',
        'team': session.scalar(select(Team)),
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()
    session.close()


@pytest.fixture(scope='function')
def token(user):
    payload = {'username':user.username, 'exp':datetime.now(tz=timezone.utc) + timedelta(hours=1)}
    token = jwt.encode(payload=payload, key=SECRET_KEY)
    yield token

@pytest.fixture(scope='function')
def invalid_token(user):
    payload = {'user_id':user.id, 'exp':datetime.now(tz=timezone.utc) - timedelta(hours=1)}
    token = jwt.encode(payload=payload, key=SECRET_KEY)
    yield token

@pytest.fixture
def customer_data(user):
    return {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "1234567890",
        "company_name": "Test Company",
        "sales_contact_id": user.id
    }


@pytest.fixture
def customer(session, customer_data):
    customer = Customer.create(session, customer_data)
    yield customer
    session.delete(customer)
    session.commit()


@pytest.fixture
def contract_data_for_validation(customer):
    """Fixture for testing validate_data method"""
    return {
        "total_balance": 1000.0,
        "remaining_balance": 500.0,
        "status": ContractStatus.CREATED.value,
        "customer_id": customer.id
    }


@pytest.fixture
def contract_data(customer):
    """Fixture for creating contracts"""
    return {
        "total_balance": 1000.0,
        "remaining_balance": 500.0,
        "status": ContractStatus.CREATED,
        "customer_id": customer.id
    }


@pytest.fixture
def contract(session, contract_data):
    contract = Contract.create(session, contract_data)
    yield contract
    session.delete(contract)
    session.commit()


@pytest.fixture
def event_data_for_validation(contract):
    """Fixture for testing validate_data method"""
    return {
        "event_start_date": "2023-01-01 12:00",
        "event_end_date": "2023-01-01 14:00",
        "location": "Test Location",
        "attendees": 50,
        "notes": "Test event notes",
        "contract_id": contract.id
    }


@pytest.fixture
def event_data(contract):
    """Fixture for creating events"""
    return {
        "event_start_date": datetime.now(timezone.utc),
        "event_end_date": datetime.now(timezone.utc) + timedelta(hours=2),
        "location": "Test Location",
        "attendees": 50,
        "notes": "Test event notes",
        "contract_id": contract.id
    }


@pytest.fixture
def event(session, event_data):
    event = Event.create(session, event_data)
    yield event
    session.delete(event)
    session.commit()
