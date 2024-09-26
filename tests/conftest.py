from datetime import datetime, timezone, timedelta

import jwt
import pytest
from passlib.handlers.argon2 import argon2
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from models import User
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



