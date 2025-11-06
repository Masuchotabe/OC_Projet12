import json
from datetime import datetime

import click
from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import Session, sessionmaker

from models import Base, User, Contract, Customer, Event
from models.contract import ContractStatus
from settings import DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST

DATABASE_URL = f'mysql+mysqldb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'


def get_engine():
    return create_engine(DATABASE_URL)


def get_session():
    engine = get_engine()
    session_factory = sessionmaker(bind=engine)
    return session_factory()


config_group = click.Group('config')


@config_group.command()
@click.option('--filename', type=click.Path(exists=False, dir_okay=False), default='fixtures/database_dump.json')
def dump_data(filename):
    tables = Base.metadata.tables.keys()
    data = {}
    engine = get_engine()
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

    engine = get_engine()
    with engine.connect() as conn:
        for table_name in ['team_table', 'user_table', 'customer_table', 'contract_table', 'event_table']:
            table = Base.metadata.tables[table_name]
            if table_name not in json_data or not json_data[table_name]:
                continue
            sql_query = insert(table).values(json_data[table_name])
            conn.execute(sql_query)
            conn.commit()


@config_group.command()
def create_sample_data():
    """Create example data for the project"""

    engine = get_engine()
    with Session(engine) as session:

        if not User.get_users(session):
            user_to_create = [
                {
                    'username': 'tmanagement',
                    'personal_number': '0123456789',
                    'first_name': 'Thomas',
                    'last_name': 'Management',
                    'email': 'tmanagement@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '1',  # management team
                },
                {
                    'username': 'jsales',
                    'personal_number': '9876543210',
                    'first_name': 'John',
                    'last_name': 'Sales',
                    'email': 'jsales@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '2',  # sales team
                },
                {
                    'username': 'msupports',
                    'personal_number': '0101010101',
                    'first_name': 'Manu',
                    'last_name': 'Supports',
                    'email': 'msupports@epicevent.com',
                    'password': 'P@ssw0rd01',
                    'phone': '',
                    'team_id': '3',  # support team
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
            for user_data in user_to_create:
                User.create(session, user_data)

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
            for customer_data in customer_to_create:
                Customer.create(session, customer_data)

        if not Contract.get_contracts(session, not_signed=False, unpaid_contracts=False):
            contract_to_create = [
                {
                    'total_balance': '2500',
                    'remaining_balance': '2500',
                    'status': ContractStatus.CREATED,
                    'customer_id': 1,
                },
                {
                    'total_balance': '4950',
                    'remaining_balance': '2000',
                    'status': ContractStatus.SIGNED,
                    'customer_id': 2,
                },
                {
                    'total_balance': '1700',
                    'remaining_balance': '0',
                    'status': ContractStatus.FINISHED,
                    'customer_id': 3,
                },
                {
                    'total_balance': '1234',
                    'remaining_balance': '1000',
                    'status': ContractStatus.CREATED,
                    'customer_id': 4,
                }
            ]
            for contract_data in contract_to_create:
                Contract.create(session, contract_data)

        if not Event.get_events(session):
            events_to_create = [
                {
                    'event_start_date': datetime(2024, 11, 5, 9, 0),
                    'event_end_date': datetime(2024, 11, 5, 17, 0),
                    'location': 'Paris',
                    'attendees': 200,
                    'notes': "Salon de l'agriculture",
                    'contract_id': 1,
                    'support_contact_id': 3,  # msupports
                },
                {
                    'event_start_date': datetime(2024, 12, 1, 10, 0),
                    'event_end_date': datetime(2024, 12, 1, 18, 0),
                    'location': 'France',
                    'attendees': 150,
                    'notes': 'Conférence en visio sur les mondes imaginaires',
                    'contract_id': 2,
                    'support_contact_id': 3,  # msupports
                },
                {
                    'event_start_date': datetime(2025, 1, 15, 8, 30),
                    'event_end_date': datetime(2025, 1, 15, 17, 30),
                    'location': 'Tours',
                    'attendees': 300,
                    'notes': 'PyCon FR',
                    'contract_id': 3,
                    'support_contact_id': None,  # Pas de support assigné
                },
                {
                    'event_start_date': datetime(2025, 2, 10, 9, 0),
                    'event_end_date': datetime(2025, 2, 10, 16, 0),
                    'location': 'Lille',
                    'attendees': 1000,
                    'notes': 'Salon du beau temps',
                    'contract_id': 4,
                    'support_contact_id': 6,  # dcoudre
                },
                {
                    'event_start_date': datetime(2025, 6, 20, 14, 0),
                    'event_end_date': datetime(2025, 6, 21, 3, 0),
                    'location': 'Château de Versailles',
                    'attendees': 500,
                    'notes': "Gala de fin d'année",
                    'contract_id': 1,
                    'support_contact_id': 3,  # msupports
                },
            ]

            for event_data in events_to_create:
                Event.create(session, event_data)
