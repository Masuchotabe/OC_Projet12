import json

from sqlalchemy import create_engine, inspect, text, insert

from models import Base
from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

DATABASE_URL = f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)


def dump_data(engine, json_file='fixtures/database_dump.json'):
    tables = Base.metadata.tables.keys()
    data = {}
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            data[table] = [row._asdict() for row in result]

    with open(json_file, 'w') as f:
        json.dump(data, f)


def load_data(engine, json_file='fixtures/database_dump.json'):
    """Permet d'intégrer des données depuis un fichier json"""
    with open(json_file, 'r') as file:
        json_data = json.load(file)

    with engine.connect() as conn:
        for table_name in ['team_table', 'user_table', 'customer_table', 'contract_table', 'event_table']:
            table = Base.metadata.tables[table_name]
            if table_name not in json_data or not json_data[table_name]:
                continue
            sql_query = insert(table).values(json_data[table_name])
            conn.execute(sql_query)
            conn.commit()

