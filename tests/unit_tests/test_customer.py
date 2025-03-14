from models import Customer


def test_customer_create(session, customer_data):
    """
    Test the creation of a new customer.

    Args:
        session (Session): The SQLAlchemy session.
        customer_data (dict): A dictionary containing customer data to be used for creation.
    """
    # Create a new customer using the provided session and customer data
    customer = Customer.create(session, customer_data)

    # Assert that the created customer's attributes match the provided data
    assert customer.name == customer_data['name']
    assert customer.email == customer_data['email']
    assert customer.company_name == customer_data['company_name']
    assert customer.phone == customer_data['phone']


def test_customer_get_customers(session):
    """
    Test retrieving a list of customers.

    Args:
        session (Session): The SQLAlchemy session.
    """
    customers = Customer.get_customers(session)
    assert len(customers) == 3
    assert customers[0].name == 'Customer 1'
    assert customers[1].name == 'Customer 2'
    assert customers[2].name == 'Customer 3'


def test_customer_get_customer(session, customer_data):
    """
    Test retrieving a customer by email.

    Args:
        session (Session): The SQLAlchemy session.
        customer_data (dict): Valid customer data.
    """
    customer = Customer.get_customer(session, customer_data['email'])
    assert customer.name == customer_data['name']
    assert customer.email == customer_data['email']
    assert customer.company_name == customer_data['company_name']
    assert customer.phone == customer_data['phone']


def test_customer_validate_data(customer_data):
    """
    Test validating customer data.

    Args:
        customer_data (dict): Valid customer data.
    """
    errors = Customer.validate_data(customer_data)
    assert len(errors) == 0
    errors = Customer.validate_data(customer_data)
    assert len(errors) == 0


def test_customer_validate_data_invalid_email(customer_data):
    """
    Test validating customer data with an invalid email.

    Args:
        customer_data (dict): Valid customer data.

    Modifies the customer data to have an invalid email and tests that the
    validation function returns an error message.
    """
    customer_data['email'] = 'invalid_email'
    errors = Customer.validate_data(customer_data)
    assert len(errors) == 1
    assert errors[0] == 'Invalid email address.'
