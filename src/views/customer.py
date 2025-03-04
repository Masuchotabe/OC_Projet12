from rich.prompt import Prompt

from .globals import display_table


def prompt_for_customer(actual_customer=None):
    """
    Prompt the user to enter or update customer data.
    Args:
        actual_customer (Customer, optional): An existing customer to edit. If None, a new customer will be created.
    Returns:
        dict: A dictionary containing the customer data entered by the user.
    """
    customer_data = {}
    if actual_customer:
        customer_data['name'] = Prompt.ask('NAme', default=actual_customer.name)
        customer_data['email'] = Prompt.ask('Email', default=actual_customer.email)
        customer_data['company_name'] = Prompt.ask('Company', default=actual_customer.company_name)
        customer_data['phone'] = Prompt.ask('Phone', default=actual_customer.phone)
        customer_data['sales_contact_username'] = Prompt.ask('Sales contact username',
                                                             default=actual_customer.sales_contact.username)
    else:
        customer_data['name'] = Prompt.ask('Name')
        customer_data['email'] = Prompt.ask('Email')
        customer_data['company_name'] = Prompt.ask('Company')
        customer_data['phone'] = Prompt.ask('Phone')

    return customer_data


def display_customers(customers):
    """
    Display a list of customers in a tabular format.
    Args:
        customers (list): A list of customer objects to display.
    """
    headers = ['Id', 'Name', 'Email', 'Phone', 'Company', 'Sales contact']
    title = "Customers" if len(customers) > 1 else "Customer"
    rows = []
    for customer in customers:
        rows.append(
            (customer.id, customer.name, customer.email, customer.phone, customer.company_name, customer.sales_contact)
        )
    display_table(headers, rows, title)
