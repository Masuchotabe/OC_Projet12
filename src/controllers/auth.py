import click
from passlib.hash import argon2
from sqlalchemy.orm import Session

from database import engine
from decorators import manage_session
from models import User
from utils import create_token
from views import show_error
from views.auth import login_view, display_token


auth_cli = click.Group()

@auth_cli.command()
@manage_session
def user_login(session):
    """Connexion d'un utilisateur"""
    username, password = login_view()
    user = session.query(User).filter_by(username=username).first()
    if user and argon2.verify(password, user.password):
        token = create_token(payload_data={"user_id": user.id})
        display_token(token)
        return
    show_error('Wrong username or password')
