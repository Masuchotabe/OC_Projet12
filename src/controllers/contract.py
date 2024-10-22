from datetime import datetime

import click
from passlib.hash import argon2

from controllers.customer import ask_for_customer
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
    if not target_contract:
        return
    print(f"{target_contract=}")
    print(f"{target_contract.customer=}")
    print(f"{target_contract.customer.sales_contact=}")
    print(f'{user=}')
    if user.has_perm('update_only_my_contracts') and target_contract.customer.sales_contact != user:
        return show_error("You don't have permission to edit this contract")

    contract_data = ask_for_contract_data(session, target_contract)
    if contract_data:
        target_contract.update(session, contract_data)

def ask_for_contract(session):
    try_again = True
    target_contract = None
    while try_again:

        target_id = ask_for('Enter the ID of the contract', output_type=int)
        if target_id:
            target_contract = Contract.get_contract(session, id=target_id)
            if target_contract:
                break
            else:
                show_error('Wrong ID.')
        try_again = ask_confirm('Try again ?')
    return target_contract

def ask_for_contract_data(session, contract=None):
    try_again = True
    contract_data = dict()
    while try_again:
        status_choices = [status.value for status in ContractStatus]
        contract_data = prompt_for_contract(contract, status_choices)

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