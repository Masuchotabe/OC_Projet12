from click.testing import CliRunner
from sqlalchemy import select

from main import global_cli


def test_user_login_command(user, monkeypatch, cli_runner):
    """Test the user-login command"""
    input_values = iter(['test_admin', 'test_password'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args,**kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['user-login'])

    assert result.exit_code == 0
    assert 'Your token is' in result.output

