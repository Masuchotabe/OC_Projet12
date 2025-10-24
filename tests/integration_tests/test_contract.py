from click.testing import CliRunner

from main import global_cli
from models.contract import ContractStatus

def test_create_contract_command(engine, session, customer, token, monkeypatch):
    """Test the create-contract command"""
    runner = CliRunner()

    # Mock user inputs for contract creation
    input_values = iter(['1000.0', '500.0', str(ContractStatus.CREATED.value), customer.email])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['create-contract', token])

    assert result.exit_code == 0
    assert 'Contract created successfully' in result.output or 'created successfully' in result.output

def test_get_contracts_command(engine, session, contract, token, monkeypatch):
    """Test the get-contracts command"""
    runner = CliRunner()

    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-contracts', token])

    assert result.exit_code == 0
    assert str(contract.id) in result.output
    assert str(contract.total_balance) in result.output

def test_get_contract_command(engine, session, contract, token, monkeypatch):
    """Test the get-contract command"""
    runner = CliRunner()

    # Mock user input for contract ID
    input_values = iter([str(contract.id)])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-contract', token])

    assert result.exit_code == 0
    assert str(contract.id) in result.output
    assert str(contract.total_balance) in result.output

def test_get_contracts_with_filters_command(engine, session, contract, token, monkeypatch):
    """Test the get-contracts command with filters"""
    runner = CliRunner()

    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    # Test with --not-signed filter
    result = runner.invoke(global_cli, ['get-contracts', token, '--not-signed'])

    assert result.exit_code == 0
    assert str(contract.id) in result.output  # Our test contract has status CREATED

    # Test with --unpaid filter
    result = runner.invoke(global_cli, ['get-contracts', token, '--unpaid'])

    assert result.exit_code == 0
    assert str(contract.id) in result.output  # Our test contract has remaining_balance > 0
