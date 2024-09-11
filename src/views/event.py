from rich.prompt import Prompt

from views import display_table


def prompt_for_event(event=None):
    event_data = {}
    if event:
        event_data['event_start_date'] = Prompt.ask('Event start date (YYYY-MM-DD HH:MM)', default=event.event_start_date.strftime('%Y-%m-%d %H:%M'))
        event_data['event_end_date'] = Prompt.ask('Event end date (YYYY-MM-DD HH:MM)', default=event.event_end_date.strftime('%Y-%m-%d %H:%M'))
        event_data['location'] = Prompt.ask('Location', default=event.location)
        event_data['attendees'] = Prompt.ask('Attendees', default=str(event.attendees))
        event_data['notes'] = Prompt.ask('Notes', default=event.notes)
        event_data['contract_id'] = Prompt.ask('Contract ID', default=str(event.contract_id))
        event_data['support_contact_username'] = Prompt.ask('Support contact username', default=event.support_contact.username if event.support_contact else None)
    else:
        event_data['event_start_date'] = Prompt.ask('Event start date (YYYY-MM-DD HH:MM)')
        event_data['event_end_date'] = Prompt.ask('Event end date (YYYY-MM-DD HH:MM)')
        event_data['location'] = Prompt.ask('Location')
        event_data['attendees'] = Prompt.ask('Attendees')
        event_data['notes'] = Prompt.ask('Notes')
        event_data['contract_id'] = Prompt.ask('Contract ID')
        event_data['support_contact_username'] = Prompt.ask('Support contact username')
    return event_data


def display_events(events):
    headers = ['ID', 'Start Date', 'End Date', 'Location', 'Attendees', 'Notes', 'Contract ID', 'Support Contact']
    title = "Events" if len(events) > 1 else "Event"
    rows = []
    for event in events:
        rows.append(
            (
                event.id,
                event.event_start_date.strftime('%Y-%m-%d %H:%M'),
                event.event_end_date.strftime('%Y-%m-%d %H:%M'),
                event.location,
                event.attendees,
                event.notes,
                event.contract_id,
                event.support_contact.username if event.support_contact else None
            )
        )
    display_table(headers, rows, title)