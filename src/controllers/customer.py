from datetime import datetime

import click
from passlib.hash import argon2

from models import Customer
from sqlalchemy.orm import Session

from database import engine
from decorators import login_required

# @click.group()
# def customer_cli():
#     pass
customer_cli = click.Group()

@customer_cli.command()
@click.argument('token')
@login_required
def create_customer(customer_data, user):
    """Création d'un client"""
    if not user.has_perm('create_customer'):
        return
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

@customer_cli.command()
@click.argument('token')
@login_required
def get_customer(customer_id, user):
    """Retourne un client à partir de son ID"""
    if not user.has_perm('get_customer'):
        return
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)
        return customer

@customer_cli.command()
@click.argument('token')
@login_required
def get_customers(user):
    """Retourne tous les clients"""
    if not user.has_perm('list_customers'):
        return
    with Session(engine) as session:
        customers = session.query(Customer).all()
        return customers

@customer_cli.command()
@click.argument('token')
@login_required
def delete_customer(customer_id, user):
    """Supprime un client"""
    if not user.has_perm('delete_customer'):
        return
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)
        session.delete(customer)
        session.commit()

@customer_cli.command()
@click.argument('token')
@login_required
def update_customer(customer_id, customer_data, user):
    """Met à jour un client"""
    if not user.has_perm('update_customer'):
        return
    with Session(engine) as session:
        customer = session.query(Customer).get(customer_id)

        customer.name = customer_data.get('name') or customer.name
        customer.email = customer_data.get('email') or customer.email
        customer.phone = customer_data.get('phone') or customer.phone
        customer.company_name = customer_data.get('company_name') or customer.company_name
        customer.date_modified = datetime.now()
        customer.sales_contact_id = customer_data.get('sales_contact_id') or customer.sales_contact_id
        session.commit()
