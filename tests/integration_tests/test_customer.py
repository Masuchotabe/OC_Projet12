from main import global_cli


def test_create_customer_command(user, token, monkeypatch, cli_runner):
    """Test the create-customer command"""
    # Mock user inputs for customer creation
    input_values = iter(['Test Integration Customer', 'integration@example.com', '1234567890', 'Integration Company'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['create-customer', token])

    assert result.exit_code == 0
    assert 'Customer created successfully' in result.output or 'created successfully' in result.output


def test_get_customers_command(customer, token, monkeypatch, cli_runner):
    """Test the get-customers command"""
    result = cli_runner.invoke(global_cli, ['get-customers', token])

    assert result.exit_code == 0
    assert customer.name in result.output
    assert customer.email in result.output


def test_get_customer_command(customer, token, monkeypatch, cli_runner):
    """Test the get-customer command"""
    # Mock user input for customer email
    input_values = iter([customer.email])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['get-customer', token])

    assert result.exit_code == 0
    assert customer.name in result.output
    assert customer.email in result.output
