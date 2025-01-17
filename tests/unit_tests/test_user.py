import pytest
from click.testing import CliRunner
from passlib.hash import argon2
from sqlalchemy import select

from controllers import create_user
from main import global_cli
from models import User
from utils import get_user_from_token

@pytest.fixture
def user_valid_data():
    return {'username': 'testuser',
            'password': 'Password123',
            'personal_number': '8754643212',
            'email': 'test@sitetest.com',
            'team_id': 1,
            }


def test_user_login(session, user, token):
    token_user = get_user_from_token(token, session)
    print(token_user)
    print(user)
    assert token_user.id == user.id


def test_user_login_command(engine, session, user, monkeypatch):

    runner = CliRunner()
    input_values = iter(['test_admin', 'test_password'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args,**kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args,**kwargs: engine)

    result = runner.invoke(global_cli, ['user-login'])
    assert result.exit_code == 0

def test_create_user(session, user_valid_data):
    """Tete user creation"""
    password = user_valid_data['password']
    user_created = User.create(session, user_valid_data)
    assert user_created.personal_number == user_valid_data['personal_number']
    assert user_created.username == user_valid_data['username']
    assert argon2.verify(password, user_created.password) == True

def test_data_validation(user_valid_data):
    user_valid_data['password'] = 'password_incorrect'
    errors = User.validate_data(user_valid_data)
    assert len(errors) == 1
