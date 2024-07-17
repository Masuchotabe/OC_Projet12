from datetime import datetime

from passlib.hash import argon2

from src.models import Customer
from sqlalchemy.orm import Session

from src.database import engine


def create_customer(customer_data):
    """Création d'un client"""
    with Session(engine) as session:
        new_customer = Customer(
            name=customer_data['name'],
            email=customer_data['email'],
            phone=customer_data.get('phone'),
            company_name=customer_data['company_name'],
            date_created=datetime.now(),
            date_modified=datetime.now(),
            sales_contact_id=customer_data['sales_contact_id']
        )
        session.add(new_customer)
        session.commit()


def get_customer(customer_id):
    """Retourne un client à partir de son ID"""
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)
        return customer


def get_customers():
    """Retourne tous les clients"""
    with Session(engine) as session:
        customers = session.query(Customer).all()
        return customers


def delete_customer(customer_id):
    """Supprime un client"""
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)
        session.delete(customer)
        session.commit()


def update_customer(customer_id, customer_data):
    """Met à jour un client"""
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)

        customer.name = customer_data.get('name') or customer.name
        customer.email = customer_data.get('email') or customer.email
        customer.phone = customer_data.get('phone') or customer.phone
        customer.company_name = customer_data.get('company_name') or customer.company_name
        customer.date_modified = datetime.now()
        customer.sales_contact_id = customer_data.get('sales_contact_id') or customer.sales_contact_id
        session.commit()
