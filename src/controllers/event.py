from datetime import datetime

from passlib.hash import argon2

from src.models import Event
from sqlalchemy.orm import Session

from src.database import engine
from utils import login_required


@login_required
def create_event(event_data, user):
    """Création d'un client"""
    if not user.has_perm('create_event'):
        return
    with Session(engine) as session:
        new_event = Event(
            event_start_date=event_data['event_start_date'],
            event_end_date=event_data['event_end_date'],
            location=event_data['location'],
            attendees=event_data['attendees'],
            notes=event_data['notes'],
            contract_id=event_data['contract_id'],
            support_contact_id=event_data['support_contact_id'],
        )
        session.add(new_event)
        session.commit()

@login_required
def get_event(event_id, user):
    """Retourne un client à partir de son ID"""
    if not user.has_perm('get_event'):
        return
    with Session(engine) as session:
        event = session.query(Event).get(event_id)
        return event

@login_required
def get_events(user):
    """Retourne tous les clients"""
    if not user.has_perm('list_events'):
        return
    with Session(engine) as session:
        events = session.query(Event).all()
        return events

@login_required
def delete_event(event_id, user):
    """Supprime un client"""
    if not user.has_perm('delete_event'):
        return
    with Session(engine) as session:
        event = session.query(Event).get(event_id)
        session.delete(event)
        session.commit()

@login_required
def update_event(event_id, event_data, user):
    """Met à jour un client"""
    if not user.has_perm('update_event'):
        return
    with Session(engine) as session:
        event = session.query(Event).get(event_id)

        event.event_start_date = event_data.get('event_start_date') or event.event_start_date
        event.event_end_date = event_data.get('event_end_date') or event.event_end_date
        event.location = event_data.get('location') or event.location
        event.attendees = event_data.get('attendees') or event.attendees
        event.notes = event_data.get('notes') or event.notes
        event.contract_id = event_data.get('contract_id') or event.contract_id
        event.support_contact_id = event_data.get('support_contact_id') or event.support_contact_id

        session.commit()
