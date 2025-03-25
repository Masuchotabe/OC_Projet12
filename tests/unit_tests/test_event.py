import pytest
from sqlalchemy import select, func
from datetime import datetime, timedelta

from models import Event, User


def test_validate_event_start_date_valid():
    """Test validate_event_start_date with valid date"""
    valid_date = "2023-01-01 12:00"
    result = Event.validate_event_start_date(valid_date)
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1
    assert result.hour == 12
    assert result.minute == 0


def test_validate_event_start_date_invalid():
    """Test validate_event_start_date with invalid date"""
    invalid_date = "2023/01/01"
    with pytest.raises(ValueError):
        Event.validate_event_start_date(invalid_date)


def test_validate_event_end_date_valid():
    """Test validate_event_end_date with valid date"""
    valid_date = "2023-01-01 14:00"
    result = Event.validate_event_end_date(valid_date)
    assert isinstance(result, datetime)
    assert result.year == 2023
    assert result.month == 1
    assert result.day == 1
    assert result.hour == 14
    assert result.minute == 0


def test_validate_event_end_date_invalid():
    """Test validate_event_end_date with invalid date"""
    invalid_date = "2023/01/01"
    with pytest.raises(ValueError):
        Event.validate_event_end_date(invalid_date)


def test_validate_data_valid(event_data_for_validation):
    """Test validate_data with valid data"""
    errors = Event.validate_data(event_data_for_validation)
    assert len(errors) == 0


def test_validate_data_invalid_date_format():
    """Test validate_data with invalid date format"""
    invalid_data = {
        "event_start_date": "2023/01/01",
        "event_end_date": "2023/01/01"
    }
    errors = Event.validate_data(invalid_data)
    assert len(errors) > 0


def test_validate_data_end_before_start(contract):
    """Test validate_data with end date before start date"""
    invalid_data = {
        "event_start_date": "2023-01-01 14:00",
        "event_end_date": "2023-01-01 12:00",
        "contract_id": contract.id
    }
    errors = Event.validate_data(invalid_data)
    assert len(errors) > 0
    assert 'Event end date must be after event start date.' in errors


def test_get_events(session, event):
    """Test get_events method"""
    events = Event.get_events(session)
    assert len(events) >= 1
    assert event in events


def test_get_events_filter_empty(session, event):
    """Test get_events method with filter_empty=True"""
    # First ensure the event has no support contact
    event.support_contact_id = None
    session.commit()

    events = Event.get_events(session, filter_empty=True)
    assert len(events) >= 1
    assert event in events


def test_get_events_user_only(session, event, user):
    """Test get_events method with user_only=True"""
    # First assign the user as support contact
    event.support_contact_id = user.id
    session.commit()

    events = Event.get_events(session, user=user, user_only=True)
    assert len(events) >= 1
    assert event in events


def test_get_event(session, event):
    """Test get_event method"""
    found_event = Event.get_event(session, event.id)
    assert found_event is not None
    assert found_event.id == event.id


def test_get_event_not_found(session):
    """Test get_event method with non-existent id"""
    non_existent_id = 9999
    event = Event.get_event(session, non_existent_id)
    assert event is None


def test_create_event(session, event_data):
    """Test create method"""
    event = Event.create(session, event_data)
    assert event is not None
    assert event.location == event_data["location"]
    assert event.attendees == event_data["attendees"]
    assert event.notes == event_data["notes"]
    assert event.contract_id == event_data["contract_id"]

    # Clean up
    session.delete(event)
    session.commit()


def test_update_event(session, event):
    """Test update method"""
    updated_data = {
        "location": "Updated Location",
        "attendees": 100,
        "notes": "Updated notes"
    }

    event.update(session, updated_data)

    # Refresh the event from the database
    session.refresh(event)

    assert event.location == updated_data["location"]
    assert event.attendees == updated_data["attendees"]
    assert event.notes == updated_data["notes"]


def test_update_data_internal(event):
    """Test _update_data internal method"""
    updated_data = {
        "location": "Internal Update",
        "attendees": 150
    }

    event._update_data(updated_data)

    assert event.location == updated_data["location"]
    assert event.attendees == updated_data["attendees"]
    # notes should be unchanged
    assert event.notes == "Test event notes"


def test_delete_event(session, event_data):
    """Test delete method"""
    event = Event.create(session, event_data)
    event_id = event.id

    # Verify event exists
    assert Event.get_event(session, event_id) is not None

    # Delete event
    event.delete(session)

    # Verify event no longer exists
    assert Event.get_event(session, event_id) is None
