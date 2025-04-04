import click
from passlib.hash import argon2

from database import get_session
# from decorators import manage_session
from models import User
from utils import create_token
from views import show_error
from views.auth import login_view, display_token


auth_cli = click.Group()

@auth_cli.command()
# @manage_session
def user_login():
    """
    Authenticate a user and generate an authentication token.
    Args:
        session(Session): SQLAlchemy session
    """
    session = get_session()
    username, password = login_view()
    user = User.get_user(session, username)
    if user and argon2.verify(password, user.password):
        token = create_token(payload_data={"username": user.username})
        display_token(token)
        return
    show_error('Wrong username or password')
