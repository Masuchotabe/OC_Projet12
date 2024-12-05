from rich.prompt import Prompt

from views import display_table


def prompt_for_contract(contract=None, status_choices=None):
    """
    Prompt the user to enter or update contract data.
    Args:
        contract (Contract, optional): An existing contract to edit. If None, a new contract will be created.
        status_choices (list, optional): A list of valid contract statuses to choose from.
    Returns:
        dict: A dictionary containing the contract data entered by the user.
    """
    contract_data = {}
    if contract:
        contract_data['total_balance'] = Prompt.ask('Total balance', default=str(contract.total_balance))
        contract_data['remaining_balance'] = Prompt.ask('Remaining balance', default=str(contract.remaining_balance))
        contract_data['status'] = Prompt.ask('Status', choices=status_choices, default=contract.status.value)
        contract_data['customer_email'] = Prompt.ask('Customer email', default=contract.customer.email if contract.customer else None)
    else:
        contract_data['total_balance'] = Prompt.ask('Total balance')
        contract_data['remaining_balance'] = Prompt.ask('Remaining balance')
        contract_data['status'] = Prompt.ask('Status', choices=status_choices)
        contract_data['customer_email'] = Prompt.ask('Customer email')
    return contract_data

def display_contracts(contracts):
    """
    Display a list of contracts in a tabular format.
    Args:
        contracts (list): A list of contract objects to display.
    """
    headers = ['ID', 'Total Balance', 'Remaining Balance', 'Status', 'Customer Email']
    title = "Contracts" if len(contracts) > 1 else "Contract"
    rows = []
    for contract in contracts:
        rows.append(
            (
                contract.id,
                contract.total_balance,
                contract.remaining_balance,
                contract.status.value,
                contract.customer.email if contract.customer else None
            )
        )
    display_table(headers, rows, title)