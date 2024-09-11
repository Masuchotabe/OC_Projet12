from datetime import datetime

import click
from passlib.hash import argon2

from models import Contract, Customer
from sqlalchemy.orm import Session

from database import engine
from decorators import login_required, manage_session, permission_required
from models.contract import ContractStatus
from views import show_error, ask_confirm, ask_for
from views.contract import display_contracts, prompt_for_contract

contract_cli = click.Group()

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_contract')
def create_contract(user, session):
    """Création d'un contrat"""
    contract_data = ask_for_contract_data(session)

    if contract_data:
        Contract.create(session, contract_data)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('get_contract')
def get_contract(user, session):
    """Retourne un contrat à partir de son ID"""
    target_contract = ask_for_contract(session)

    if target_contract:
        display_contracts([target_contract])

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_contracts')
def get_contracts(user, session):
    """Retourne tous les contrats"""
    contracts = Contract.get_contracts(session)
    display_contracts(contracts)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_contract')
def delete_contract(user, session):
    """Supprime un contrat"""
    target_contract = ask_for_contract(session)

    if target_contract:
        target_contract.delete(session)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_contract')
def update_contract(user, session):
    """Met à jour un contrat"""
    target_contract = ask_for_contract(session)

    contract_data = ask_for_contract_data(session, target_contract)
    if contract_data:
        target_contract.update(session, contract_data)

def ask_for_contract(session):
    is_valid = False
    target_contract = None
    while not is_valid:
        try:
            target_id = int(ask_for('Enter the ID of the contract')[0])
        except ValueError:
            show_error('ID must be an integer. Please try again.')
            continue

        if target_id:
            target_contract = Contract.get_contract(session, id=target_id)
            if target_contract:
                is_valid = True
            else:
                show_error('Wrong ID, try again.')
    return target_contract

def ask_for_contract_data(session, contract=None):
    try_again = True
    contract_data = dict()
    while try_again:
        status_choices = [status.value for status in ContractStatus]
        contract_data = prompt_for_contract(contract, status_choices)

        # Validation spécifique à Contract (à implémenter dans le modèle Contract)
        errors = Contract.validate_data(contract_data)

        if contract_data['customer_email'] and not Customer.get_customer(session, email=contract_data['customer_email']):
            errors.append('Wrong customer email.')
        elif contract_data['customer_email']:
            contract_data['customer'] = Customer.get_customer(session, email=contract_data['customer_email'])

        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_confirm('Try again ?')
    return contract_data