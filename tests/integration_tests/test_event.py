from datetime import datetime, timedelta

from main import global_cli


def test_create_event_command(session, contract, token, monkeypatch, cli_runner):
    """Test the create-event command"""
    # Mock user inputs for event creation
    start_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    end_date = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    input_values = iter([start_date, end_date, 'Test Location', '50', 'Test notes', str(contract.id), ''])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))

    # Set contract status to SIGNED for the test
    contract.status = 'SIGNED'
    session.commit()

    result = cli_runner.invoke(global_cli, ['create-event', token])

    assert result.exit_code == 0
    assert 'Event created successfully' in result.output or 'created successfully' in result.output


def test_get_events_command(event, token, cli_runner):
    """Test the get-events command"""
    result = cli_runner.invoke(global_cli, ['get-events', token])

    assert result.exit_code == 0
    assert str(event.id) in result.output
    assert event.location in result.output


def test_get_event_command(event, token, monkeypatch, cli_runner):
    """Test the get-event command"""
    # Mock user input for event ID
    input_values = iter([str(event.id)])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['get-event', token])

    assert result.exit_code == 0
    assert str(event.id) in result.output
    assert event.location in result.output


def test_get_events_with_filters_command(session, event, user, token, cli_runner):
    """Test the get-events command with filters"""
    # Set event support contact to None for the test
    event.support_contact_id = None
    session.commit()

    # Test with --filter-empty-support filter
    result = cli_runner.invoke(global_cli, ['get-events', token, '--filter-empty-support'])

    assert result.exit_code == 0
    assert str(event.id) in result.output

    # Set event support contact to user for the test
    event.support_contact_id = user.id
    session.commit()

    # Test with --my-events filter
    result = cli_runner.invoke(global_cli, ['get-events', token, '--my-events'])

    assert result.exit_code == 0
    assert str(event.id) in result.output
