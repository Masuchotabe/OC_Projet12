from sqlalchemy import create_engine

from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

DATABASE_URL = f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)