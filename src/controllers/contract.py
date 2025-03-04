from datetime import datetime

import click
from passlib.hash import argon2

from models import Contract, Customer
from sqlalchemy.orm import Session

from decorators import login_required, manage_session, permission_required
from models.contract import ContractStatus
from views import show_error, ask_for
from views.contract import display_contracts, prompt_for_contract

contract_cli = click.Group()

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_contract')
def create_contract(user, session):
    """
    Create contract.
    Args:
        user(User): connected user from token
        session(Session): Sqlalchemy session
    """
    contract_data = ask_for_contract_data(session)

    if contract_data:
        Contract.create(session, contract_data)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('get_contract')
def get_contract(user, session):
    """
    Display a contract selected by ID.
    Args:
        user(User): connected user from token
        session(Session): Sqlalchemy session
    """
    target_contract = ask_for_contract(session)

    if target_contract:
        display_contracts([target_contract])

@contract_cli.command()
@click.argument('token')
@click.option('--not-signed', default=False, is_flag=True)
@click.option('--unpaid', default=False, is_flag=True)
@manage_session
@login_required
@permission_required('list_contracts')
def get_contracts(user, session, not_signed, unpaid):
    """
    Display list of contract.
    Args:
        user(User): connected user from token
        session(Session): Sqlalchemy session
        not_signed(bool): display contract not signed
        unpaid(bool): Display not fully paid contract
    """
    contracts = Contract.get_contracts(session, not_signed, unpaid)
    display_contracts(contracts)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_contract')
def delete_contract(user, session):
    """
    Delete contract.
    Args:
        user(User): connected user from token
        session(Session): Sqlalchemy session
    """
    target_contract = ask_for_contract(session)

    if target_contract:
        target_contract.delete(session)

@contract_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_contract')
def update_contract(user, session):
    """
    Update contract.
    Args:
        user(User): connected user from token
        session(Session): Sqlalchemy session
    """

    target_contract = ask_for_contract(session)
    if not target_contract:
        return

    if user.has_perm('update_only_my_contracts') and target_contract.customer.sales_contact != user:
        show_error("You don't have permission to edit this contract")
        return

    contract_data = ask_for_contract_data(session, target_contract)
    if contract_data:
        target_contract.update(session, contract_data)

def ask_for_contract(session):
    """
    Ask for contract by ID.
    Args:
        session(Session): Sqlalchemy session
    Returns(Contract or None): Contract or None
    """
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
        try_again = ask_for('Try again ?', output_type=bool)
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
        try_again = ask_for('Try again ?', output_type=bool)
    return contract_data