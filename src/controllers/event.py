import click

from models import Event, Contract, User
from sqlalchemy.orm import Session

from decorators import login_required, manage_session, permission_required
from models.contract import ContractStatus
from views import show_error, ask_for, ask_confirm
from views.event import prompt_for_event, display_events

event_cli = click.Group()

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_event')
def create_event(user, session):
    """
    Create a new event.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    event_data = ask_for_event_data(session, user)
    contract = event_data.get('contract')

    if contract and contract.customer.sales_contact != user:
        return show_error(f"You don't have permission to add events to this contract (client {contract.customer})")
    elif contract and contract.status != ContractStatus.SIGNED:
        return show_error("Contract must be signed.")

    if event_data:
        Event.create(session, event_data)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('get_event')
def get_event(user, session):
    """
    Retrieve and display an event by ID.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_event = ask_for_event(session)
    if target_event:
        display_events([target_event])

@event_cli.command()
@click.argument('token')
@click.option('--filter-empty-support', default=False, is_flag=True)
@click.option('--my-events', default=False, is_flag=True)
@manage_session
@login_required
@permission_required('list_events')
def get_events(user, session, filter_empty_support, my_events):
    """
    Retrieve and display a list of events.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
        filter_empty_support(bool): filter events without support contact
        my_events(bool): filter only events related to the current user
    """
    events = Event.get_events(session, user, filter_empty_support, my_events)
    display_events(events)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_event')
def delete_event(user, session):
    """
    Delete an event by ID.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_event = ask_for_event(session)
    if target_event:
        target_event.delete(session)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_event')
def update_event(user, session):
    """
    Update an existing event.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_event = ask_for_event(session)
    if user.has_perm('update_only_my_events') and target_event.support_contact != user:
        return show_error("You don't have permission to edit this event")
    event_data = ask_for_event_data(session, user, target_event)
    if event_data:
        target_event.update(session, event_data)

def ask_for_event(session):
    """
    Prompt user for an event ID and retrieve the event.
    Args:
        session(Session): SQLAlchemy session
    Returns(Event or None): Event instance or None if not found
    """
    try_again = True
    target_event = None
    while try_again:
        target_id = ask_for('Enter the ID of the event', output_type=int)
        if target_id:
            target_event = Event.get_event(session, id=target_id)
            if target_event:
                break
            else:
                show_error('Wrong ID.')
        try_again = ask_confirm('Try again?')
    return target_event

def ask_for_event_data(session, user, event=None):
    """
    Prompt user for event data and validate it.
    Args:
        session(Session): SQLAlchemy session
        user(User): connected user
        event(Event, optional): existing event instance
    Returns(dict): validated event data
    """
    try_again = True
    while try_again:
        event_data = prompt_for_event(user, event)
        errors = Event.validate_data(event_data)

        if event_data['contract_id'] and not Contract.get_contract(session, id=event_data['contract_id']):
            errors.append('Wrong contract ID.')
        elif event_data['contract_id']:
            event_data['contract'] = Contract.get_contract(session, id=event_data['contract_id'])
        elif not event and not event_data['contract_id']:
            errors.append('You must enter a contract ID.')

        if event_data['support_contact_username'] and not User.get_user(session, event_data['support_contact_username']):
            errors.append('Wrong username for support contact.')
        elif event_data['support_contact_username']:
            event_data['support_contact'] = User.get_user(session, event_data['support_contact_username'])

        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_confirm('Try again?')
    return event_data
