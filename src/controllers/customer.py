import click

from models import Customer, User

from decorators import login_required, manage_session, permission_required
from views import show_error, ask_confirm, ask_for
from views.customer import prompt_for_customer, display_customers

customer_cli = click.Group()

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_customer')
def create_customer(user, session):
    """Création d'un client"""
    customer_data = ask_for_customer_data(session)
    customer_data['sales_contact'] = user

    if customer_data:
        Customer.create(session, customer_data)


@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('get_customer')
def get_customer(user, session):
    """Retourne un client à partir de son ID"""
    target_customer = ask_for_customer(session)

    if target_customer:
        display_customers([target_customer])

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_customers')
def get_customers(user, session):
    """Retourne tous les clients"""
    customers = Customer.get_customers(session)
    display_customers(customers)

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_customers')
def delete_customer(user, session):
    """Supprime un client"""
    target_customer = ask_for_customer(session)

    if target_customer:
        target_customer.delete()

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_customer')
def update_customer(user, session):
    """Met à jour un client"""
    target_customer = ask_for_customer(session)

    customer_data = ask_for_customer_data(session, target_customer)
    if customer_data:
        target_customer.update(session, customer_data)

def ask_for_customer(session):
    is_valid = False
    target_customer = None
    while not is_valid:
        target_email, stop = ask_for('Enter the email of the customer')
        if stop:
            break
        target_customer = Customer.get_customer(session, email=target_email)
        if target_customer:
            is_valid = True
        else:
            show_error('Wrong username, try again.')
    return target_customer

def ask_for_customer_data(session, customer=None):
    try_again = True
    customer_data = dict()
    while try_again:

        customer_data = prompt_for_customer(customer)
        errors = Customer.validate_data(customer_data)
        if customer_data.get('sales_contact_username') and not User.get_user(session,customer_data['sales_contact_username']):
            errors.append('Wrong username for sales contact.')
        elif customer_data.get('sales_contact_username'):
            customer_data['sales_contact'] = User.get_user(session, customer_data['sales_contact_username'])

        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_confirm('Try again ?')
    return customer_data