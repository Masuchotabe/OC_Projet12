from click.testing import CliRunner
from sqlalchemy import select

from main import global_cli

def test_user_login_command(engine, session, user, monkeypatch):
    """Test the user-login command"""
    runner = CliRunner()
    input_values = iter(['test_admin', 'test_password'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args,**kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args,**kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args,**kwargs: session)

    result = runner.invoke(global_cli, ['user-login'])

    assert result.exit_code == 0
    assert 'Your token is' in result.output

def test_get_users_command(engine, session, user, token, monkeypatch):
    """Test the get-users command"""
    runner = CliRunner()

    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-users', token])

    assert result.exit_code == 0
    assert user.username in result.output
    assert user.email in result.output

def test_get_user_command(engine, session, user, token, monkeypatch):
    """Test the get-user command"""
    runner = CliRunner()

    # Mock user input for username
    input_values = iter([user.username])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['get-user', token])

    assert result.exit_code == 0
    assert user.username in result.output
    assert user.email in result.output

def test_create_user_command(engine, session, token, monkeypatch):
    """Test the create-user command"""
    runner = CliRunner()

    # Mock user inputs for user creation
    # Format: username, password, personal_number, email, team_name
    input_values = iter(['test_integration_user', 'Password123', '1234567890', 'integration@example.com', 'Management team'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['create-user', token])

    assert result.exit_code == 0
    assert 'User created successfully' in result.output or 'created successfully' in result.output

def test_update_user_command(engine, session, user, token, monkeypatch):
    """Test the update-user command"""
    runner = CliRunner()

    # Mock user inputs for user update
    # Format: username to update, new username, new password (empty to keep), new personal_number, new email, new team_name
    input_values = iter([user.username, 'updated_username', '', '9876543210', 'updated@example.com', 'Management team', 'y'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['update-user', token])

    assert result.exit_code == 0
    assert 'User updated successfully' in result.output or 'updated successfully' in result.output

    # Reset the user for other tests
    user.username = 'test_admin'
    user.personal_number = '0000000000'
    user.email = 'admin@email.com'
    session.commit()

def test_delete_user_command(engine, session, token, monkeypatch):
    """Test the delete-user command"""
    runner = CliRunner()

    # First create a user to delete
    from models import User, Team
    from passlib.handlers.argon2 import argon2

    # Create a test user to delete
    user_data = {
        'username': 'user_to_delete',
        'password': argon2.hash('test_password'),
        'personal_number': '1111111111',
        'email': 'delete@example.com',
        'team': session.scalar(select(Team)),
    }
    user_to_delete = User(**user_data)
    session.add(user_to_delete)
    session.commit()

    # Mock user input for username to delete
    input_values = iter(['user_to_delete', 'y'])
    monkeypatch.setattr('rich.prompt.Prompt.ask', lambda *args, **kwargs: next(input_values))
    monkeypatch.setattr('database.get_engine', lambda *args, **kwargs: engine)
    monkeypatch.setattr('database.get_session', lambda *args, **kwargs: session)

    result = runner.invoke(global_cli, ['delete-user', token])

    assert result.exit_code == 0
    assert 'User deleted successfully' in result.output or 'deleted successfully' in result.output
