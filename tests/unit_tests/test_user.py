from click.testing import CliRunner
from sqlalchemy import select

from src.controllers import create_user
from src.models import User
from src.utils import get_user_from_token


def test_user_login(session, user, token):
    token_user = get_user_from_token(token, session)
    assert token_user.id == user.id

def test_create_user(session, token):
    # TODO : change to test the create methode of user
    # runner = CliRunner()
    # result = runner.invoke(create_user, [token, ], catch_exceptions=False)

    # result = runner.invoke(create_user, {})
    assert result.exit_code == 0