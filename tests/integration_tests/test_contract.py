from main import global_cli
from models.contract import ContractStatus, Contract


def test_create_contract_command(session, customer, token_factory, management_user, monkeypatch, cli_runner):
    """Test the create-contract command"""
    # Mock user inputs for contract creation
    input_values = iter([1000.0, 500.0, ContractStatus.CREATED.value, customer.email])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args, **kwargs: next(input_values))
    contracts_number = len(Contract.get_contracts(session, False, False))
    token = token_factory(management_user)
    result = cli_runner.invoke(global_cli, ['create-contract', token])

    assert result.exit_code == 0
    assert len(Contract.get_contracts(session, False, False)) == contracts_number+1


def test_get_contracts_command(contract, token_factory, user, monkeypatch, cli_runner):
    """Test the get-contracts command"""
    token = token_factory(user)
    result = cli_runner.invoke(global_cli, ['get-contracts', token])

    assert result.exit_code == 0
    assert str(contract.id) in result.output
    assert str(contract.total_balance) in result.output


def test_get_contract_command(contract, token_factory, user, monkeypatch, cli_runner):
    """Test the get-contract command"""
    # Mock user input for contract ID
    input_values = iter([contract.id])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args, **kwargs: next(input_values))

    token = token_factory(user)
    result = cli_runner.invoke(global_cli, ['get-contract', token])

    assert result.exit_code == 0
    assert str(contract.id) in result.output
    assert str(contract.total_balance) in result.output


def test_get_contracts_with_filters_command(contract, token_factory, user, monkeypatch, cli_runner):
    """Test the get-contracts command with filters"""
    token = token_factory(user)
    # Test with --not-signed filter
    result = cli_runner.invoke(global_cli, ['get-contracts', token, '--not-signed'])

    assert result.exit_code == 0
    assert str(contract.id) in result.output  # Our test contract has status CREATED

    # Test with --unpaid filter
    result = cli_runner.invoke(global_cli, ['get-contracts', token, '--unpaid'])

    assert result.exit_code == 0
    assert str(contract.id) in result.output  # Our test contract has remaining_balance > 0
