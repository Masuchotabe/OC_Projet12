from datetime import datetime, timedelta

from main import global_cli


def test_create_event_command(session, contract, token_factory, sales_user, monkeypatch, cli_runner):
    """Test the create-event command"""
    # Mock user inputs for event creation
    start_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    end_date = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")
    input_values = iter([start_date, end_date, 'Test Location', '50', 'Test notes', str(contract.id), ''])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args, **kwargs: next(input_values))

    # Set contract status to SIGNED for the test
    contract.status = 'SIGNED'
    session.commit()

    token = token_factory(sales_user)
    result = cli_runner.invoke(global_cli, ['create-event', token])

    assert result.exit_code == 0
    assert 'Event created successfully' in result.output or 'created successfully' in result.output
