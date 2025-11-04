from datetime import datetime, timezone, timedelta

import jwt
import pytest
from click.testing import CliRunner
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
def management_user(session):
    """User dans l'équipe Management"""
    team = session.scalar(select(Team).where(Team.name == "Management team"))
    user_data = {
        'username': 'manager_user',
        'password': argon2.hash('test_password'),
        'personal_number': '1111111111',
        'email': 'manager@email.com',
        'team': team,
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()


@pytest.fixture(scope='function')
def sales_user(session):
    """User dans l'équipe Sales"""
    team = session.scalar(select(Team).where(Team.name == "Sales team"))
    user_data = {
        'username': 'sales_user',
        'password': argon2.hash('test_password'),
        'personal_number': '2222222222',
        'email': 'sales@email.com',
        'team': team,
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()


@pytest.fixture(scope='function')
def support_user(session):
    """User dans l'équipe Support"""
    team = session.scalar(select(Team).where(Team.name == "Support team"))
    user_data = {
        'username': 'support_user',
        'password': argon2.hash('test_password'),
        'personal_number': '3333333333',
        'email': 'support@email.com',
        'team': team,
    }
    user = User(**user_data)
    session.add(user)
    session.commit()
    yield user
    session.delete(user)
    session.commit()


@pytest.fixture(scope='function')
def cli_runner():
    """Fixture pour l'exécution des commandes CLI."""
    return CliRunner()


@pytest.fixture(scope='function', autouse=True)
def use_test_database(engine, session, monkeypatch):
    """Fixture pour utiliser la BDD de test"""
    monkeypatch.setattr('database.get_engine', lambda *args,**kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args,**kwargs: session)


@pytest.fixture(scope='function')
def token_factory():
    """
    Factory pour créer des tokens à la demande pour n'importe quel user.

    Usage:
        token = token_factory(user)
        expired_token = token_factory(user, expired=True)
        custom_token = token_factory(user, hours=24)
    """
    def _create_token(user, expired=False, hours=1, **extra_payload):
        """
        Créer un token pour un user.

        Args:
            user: L'objet User
            expired: Si True, créer un token expiré
            hours: Nombre d'heures avant expiration
            **extra_payload: Données additionnelles dans le payload

        Returns:
            str: Le token JWT
        """
        if expired:
            exp_time = datetime.now(tz=timezone.utc) - timedelta(hours=1)
        else:
            exp_time = datetime.now(tz=timezone.utc) + timedelta(hours=hours)

        payload = {
            'username': user.username,
            'exp': exp_time,
            **extra_payload
        }

        return jwt.encode(payload=payload, key=SECRET_KEY)

    return _create_token


# @pytest.fixture(scope='function')
# def invalid_token(user):
#     payload = {'user_id':user.id, 'exp':datetime.now(tz=timezone.utc) - timedelta(hours=1)}
#     token = jwt.encode(payload=payload, key=SECRET_KEY)
#     yield token


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
        "customer": customer
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
