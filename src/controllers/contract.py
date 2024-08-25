from datetime import datetime

import click
from passlib.hash import argon2

from models import Contract
from sqlalchemy.orm import Session

from database import engine
from decorators import login_required

contract_cli = click.Group()


@contract_cli.command()
@click.argument('token')
@login_required
def create_contract(contract_data, user):
    """Création d'un client"""
    if not user.has_perm('create_contract'):
        return
    with Session(engine) as session:
        new_contract = Contract(
            total_balance=contract_data['total_balance'],
            remaining_balance=contract_data['remaining_balance'],
            status=contract_data['status'],
            customer_id=contract_data['customer_id']
        )
        session.add(new_contract)
        session.commit()

@contract_cli.command()
@click.argument('token')
@login_required
def get_contract(contract_id, user):
    """Retourne un client à partir de son ID"""
    if not user.has_perm('get_contract'):
        return
    with Session(engine) as session:
        contract = session.query(Contract).get(contract_id)
        return contract

@contract_cli.command()
@click.argument('token')
@login_required
def get_contracts(user):
    """Retourne tous les clients"""
    if not user.has_perm('list_contracts'):
        return
    with Session(engine) as session:
        contracts = session.query(Contract).all()
        return contracts

@contract_cli.command()
@click.argument('token')
@login_required
def delete_contract(contract_id, user):
    """Supprime un client"""
    if not user.has_perm('delete_contract'):
        return
    with Session(engine) as session:
        contract = session.query(Contract).get(contract_id)
        session.delete(contract)
        session.commit()

@contract_cli.command()
@click.argument('token')
@login_required
def update_contract(contract_id, contract_data, user):
    """Met à jour un client"""
    if not user.has_perm('update_contract'):
        return
    with Session(engine) as session:
        contract = session.query(Contract).get(contract_id)

        contract.total_balance = contract_data.get('total_balance') or contract.total_balance
        contract.remaining_balance = contract_data.get('remaining_balance') or contract.remaining_balance
        contract.status = contract_data.get('status') or contract.status
        contract.customer_id = contract_data.get('customer_id') or contract.customer_id
        session.commit()
