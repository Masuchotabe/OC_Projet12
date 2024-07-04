from sqlalchemy import create_engine

from src.models import Base

username = 'test_user'
password = 'test_password'
host = 'localhost'
database = 'test'
DATABASE_URL = f'mysql+mysqldb://{username}:{password}@{host}/{database}'

engine = create_engine(DATABASE_URL)


def create_all():
    Base.metadata.create_all(bind=engine)