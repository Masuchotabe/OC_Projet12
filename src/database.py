import json

import click
from sqlalchemy import create_engine, inspect, text, insert
from sqlalchemy.orm import Session

from models import Base, User, Contract, Customer, Event
from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

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

def create_sample_data():
    """Create example data for the project"""

    with Session(engine) as session:

        if not User.get_users(session):
            user_to_create = [
                {
                    'username': 'tmanagement',
                    'personal_number': '01234536789',
                    'first_name': 'Thomas',
                    'last_name': 'Management',
                    'email': 'tmanagement@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '1', # management team
                },
                {
                    'username': 'jsales',
                    'personal_number': '9876543210',
                    'first_name': 'John',
                    'last_name': 'Sales',
                    'email': 'jsales@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '2', # sales team
                },
                {
                    'username': 'msupports',
                    'personal_number': '0101010101',
                    'first_name': 'Manu',
                    'last_name': 'Supports',
                    'email': 'msupports@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '3', # support team
                },
                {
                    'username': 'porth',
                    'personal_number': '2345678901',
                    'first_name': 'Poire',
                    'last_name': 'Orth',
                    'email': 'porth@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '1',
                },
                {
                    'username': 'avendre',
                    'personal_number': '9988776655',
                    'first_name': 'Alonzo',
                    'last_name': 'Vendre',
                    'email': 'avendre@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '2',
                },
                {
                    'username': 'dcoudre',
                    'personal_number': '5544667733',
                    'first_name': 'Didier',
                    'last_name': 'Coudre',
                    'email': 'dcoudre@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '3',
                },
            ]
            for user in user_to_create:
                User.create(session, **user)

        if not Customer.get_customers(session):
            customer_to_create = [
                {
                    'name': 'Alfred Trop',
                    'email': 'atrop@customer.com',
                    'phone': '',
                    'company_name': 'Customer Enterprise',
                    'sales_contact_id': 1,
                },
                {
                    'name': 'Rives Jean',
                    'email': 'jrives@boat.fr',
                    'phone': '',
                    'company_name': 'Boat sas',
                    'sales_contact_id': 1,
                },
                {
                    'name': 'Peter Pan',
                    'email': 'peterp@imagine.com',
                    'phone': '01 02 03 04 05',
                    'company_name': 'Crochet sas',
                    'sales_contact_id': 2,
                },
                {
                    'name': 'Fée Clochette',
                    'email': 'feec@imagine.com',
                    'phone': '',
                    'company_name': 'Crochet sas',
                    'sales_contact_id': 2,
                }
            ]



