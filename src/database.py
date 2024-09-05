import json

import click
from sqlalchemy import create_engine, inspect, text, insert

from src.models import Base
from src.settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

DATABASE_URL = f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(DATABASE_URL)

config_group = click.Group('config')

@config_group.command()
@click.option('--filename', type=click.Path(exists=False, dir_okay=False), default='fixtures/database_dump.json')
def dump_data(filename):
    tables = Base.metadata.tables.keys()
    data = {}
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT * FROM {table}"))
            data[table] = [row._asdict() for row in result]

    with open(filename, 'w') as f:
        json.dump(data, f)

@config_group.command()
@click.option('--filename', type=click.Path(exists=True, dir_okay=False), default='fixtures/init_data.json')
def load_data(filename):
    """Permet d'intégrer des données depuis un fichier json"""
    with open(filename, 'r') as file:
        json_data = json.load(file)

    with engine.connect() as conn:
        for table_name in ['team_table', 'user_table', 'customer_table', 'contract_table', 'event_table']:
            table = Base.metadata.tables[table_name]
            if table_name not in json_data or not json_data[table_name]:
                continue
            sql_query = insert(table).values(json_data[table_name])
            conn.execute(sql_query)
            conn.commit()

