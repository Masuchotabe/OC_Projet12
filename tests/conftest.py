import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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
    session = Session(bind=engine)
    yield session

