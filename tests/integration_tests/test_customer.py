from sqlalchemy import select
from sqlalchemy.sql.functions import func

from main import global_cli
from models import Customer


def test_create_customer_command(session, sales_user, token_factory, monkeypatch, cli_runner):
    """Test the create-customer command"""
    # Mock user inputs for customer creation
    input_values = iter(['Test Integration Customer', 'integration@example.com', '1234567890', 'Integration Company'])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args, **kwargs: next(input_values))
    nb_customers_before_create = session.scalar(select(func.count()).select_from(Customer))
    token = token_factory(sales_user)
    result = cli_runner.invoke(global_cli, ['create-customer', token])
    nb_customers_after_create = session.scalar(select(func.count()).select_from(Customer))
    assert result.exit_code == 0
    assert 'Customer created successfully' in result.output
    assert nb_customers_before_create + 1 == nb_customers_after_create



# def test_get_customers_command(customer, token_factory, user, monkeypatch, cli_runner):
#     """Test the get-customers command"""
#     token = token_factory(user)
#     result = cli_runner.invoke(global_cli, ['get-customers', token])
#
#     assert result.exit_code == 0
#     assert customer.name in result.output
#     assert customer.email in result.output


def test_get_customer_command(customer, token_factory, user, monkeypatch, cli_runner):
    """Test the get-customer command"""
    # Mock user input for customer email
    input_values = iter([customer.email])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args, **kwargs: next(input_values))

    token = token_factory(user)
    result = cli_runner.invoke(global_cli, ['get-customer', token])

    assert result.exit_code == 0
    assert customer.name in result.output
    assert customer.email in result.output
