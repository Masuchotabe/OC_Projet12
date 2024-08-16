import click
from passlib.hash import argon2
from sqlalchemy.orm import Session

from database import engine
from models import User
from utils import create_token


@click.group()
def auth_cli():
    pass

@auth_cli.command()
@click.argument('username')
@click.argument('password')
def user_login(username, password):
    """"""
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            if argon2.verify(password, user.password):
                token = create_token(payload_data={"user_id": user.id})
                print(token)
            else:
                return 'Wrong password'
        else:
            return 'User does not exist'