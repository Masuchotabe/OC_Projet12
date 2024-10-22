from datetime import datetime

import click
from passlib.hash import argon2

from models import Event, Contract, User
from sqlalchemy.orm import Session

from database import engine
from decorators import login_required, manage_session, permission_required
from views import show_error, ask_for, ask_confirm
from views.event import prompt_for_event, display_events

# @click.group()
# def event_cli():
#     pass

event_cli = click.Group()


@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_event')
def create_event(user, session):
    """Création d'un événement"""
    event_data = ask_for_event_data(session)

    if event_data:
        Event.create(session, event_data)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('get_event')
def get_event(user, session):
    """Retourne un événement à partir de son ID"""
    target_event = ask_for_event(session)

    if target_event:
        display_events([target_event])

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_events')
def get_events(user, session):
    """Retourne tous les événements"""
    events = Event.get_events(session)
    display_events(events)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_event')
def delete_event(user, session):
    """Supprime un événement"""
    target_event = ask_for_event(session)

    if target_event:
        target_event.delete(session)

@event_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_event')
def update_event(user, session):
    """Met à jour un événement"""
    target_event = ask_for_event(session)
    if user.has_perm('update_only_my_events') and target_event.support_contact != user:
        return show_error("You don't have permission to edit this event")
    event_data = ask_for_event_data(session, target_event)
    if event_data:
        target_event.update(session, event_data)

def ask_for_event(session):
    is_valid = False
    target_event = None
    while not is_valid:
        try:
            target_id = int(ask_for('Enter the ID of the event')[0])
        except ValueError:
            show_error('ID must be an integer. Please try again.')
            continue

        if target_id:
            target_event = Event.get_event(session, id=target_id)
            if target_event:
                is_valid = True
            else:
                show_error('Wrong ID, try again.')
    return target_event

def ask_for_event_data(session, event=None):
    try_again = True
    event_data = dict()
    while try_again:
        event_data = prompt_for_event(event)

        errors = Event.validate_data(event_data)

        if event_data['contract_id'] and not Contract.get_contract(session, id=event_data['contract_id']):
            errors.append('Wrong contract ID.')
        elif event_data['contract_id']:
            event_data['contract'] = Contract.get_contract(session, id=event_data['contract_id'])

        if event_data['support_contact_username'] and not User.get_user(session, event_data['support_contact_username']):
            errors.append('Wrong username for support contact.')
        elif event_data['support_contact_username']:
            event_data['support_contact'] = User.get_user(session, event_data['support_contact_username'])

        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_confirm('Try again ?')
    return event_data