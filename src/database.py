import json

from sqlalchemy import create_engine, inspect, text

from models import Base
from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

DATABASE_URL = f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)


def dump_data(engine):
    # inspector = inspect(engine)
    # tables = inspector.get_table_names()
    tables = Base.metadata.tables.keys()
    # print(tables)
    data = {}
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            data[table] = [row._asdict() for row in result]

    with open('database_dump.json', 'w') as f:
        json.dump(data, f)
