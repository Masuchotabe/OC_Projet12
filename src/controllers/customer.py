import click

from models import Customer, User

from decorators import login_required, permission_required, manage_session
from views import show_error, ask_for
from views.customer import prompt_for_customer, display_customers

customer_cli = click.Group()

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_customer')
def create_customer(user, session):
    """
    Create a new customer.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    customer_data = ask_for_customer_data(session)
    customer_data['sales_contact'] = user

    if customer_data:
        Customer.create(session, customer_data)

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('read_customer')
def get_customer(user, session):
    """
    Retrieve and display a customer by email.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_customer = ask_for_customer(session)
    if target_customer:
        display_customers([target_customer])

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_customers')
def get_customers(user, session):
    """
    Retrieve and display a list of customers.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    customers = Customer.get_customers(session)
    display_customers(customers)

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_customers')
def delete_customer(user, session):
    """
    Delete a customer by email.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_customer = ask_for_customer(session)
    if target_customer:
        target_customer.delete()

@customer_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_customer')
def update_customer(user, session):
    """
    Update an existing customer's information.
    Args:
        user(User): connected user from token
        session(Session): SQLAlchemy session
    """
    target_customer = ask_for_customer(session)
    if user.has_perm('update_only_my_customers') and target_customer.sales_contact != user:
        return show_error("You don't have permission to edit this customer")
    customer_data = ask_for_customer_data(session, target_customer)
    if customer_data:
        target_customer.update(session, customer_data)

def ask_for_customer(session):
    """
    Prompt user for a customer's email and retrieve the customer.
    Args:
        session(Session): SQLAlchemy session
    Returns(Customer or None): Customer instance or None if not found
    """
    try_again = True
    target_customer = None
    while try_again:
        target_email = ask_for('Enter the email of the customer')
        if target_email:
            target_customer = Customer.get_customer(session, email=target_email)
            if target_customer:
                break
            else:
                show_error('Wrong email.')
        try_again = ask_for('Try again ?', output_type=bool)
    return target_customer

def ask_for_customer_data(session, customer=None):
    """
    Prompt user for customer data and validate it.
    Args:
        session(Session): SQLAlchemy session
        customer(Customer, optional): existing customer instance
    Returns(dict): validated customer data
    """
    try_again = True
    customer_data = dict()
    while try_again:
        customer_data = prompt_for_customer(customer)
        errors = Customer.validate_data(customer_data)

        if customer_data.get('sales_contact_username') and not User.get_user(session, customer_data['sales_contact_username']):
            errors.append('Wrong username for sales contact.')
        elif customer_data.get('sales_contact_username'):
            customer_data['sales_contact'] = User.get_user(session, customer_data['sales_contact_username'])

        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_for('Try again ?', output_type=bool)
    return customer_data
