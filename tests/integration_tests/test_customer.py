from click.testing import CliRunner

from main import global_cli

def test_create_customer_command(engine, session, user, token, monkeypatch):
    """Test the create-customer command"""
    runner = CliRunner()

    # Mock user inputs for customer creation
    input_values = iter(['Test Integration Customer', 'integration@example.com', '1234567890', 'Integration Company'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['create-customer', token])

    assert result.exit_code == 0
    assert 'Customer created successfully' in result.output or 'created successfully' in result.output

def test_get_customers_command(engine, session, customer, token, monkeypatch):
    """Test the get-customers command"""
    runner = CliRunner()

    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-customers', token])

    assert result.exit_code == 0
    assert customer.name in result.output
    assert customer.email in result.output

def test_get_customer_command(engine, session, customer, token, monkeypatch):
    """Test the get-customer command"""
    runner = CliRunner()

    # Mock user input for customer email
    input_values = iter([customer.email])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-customer', token])

    assert result.exit_code == 0
    assert customer.name in result.output
    assert customer.email in result.output
