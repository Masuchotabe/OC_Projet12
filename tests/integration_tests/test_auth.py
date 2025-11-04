from main import global_cli


def test_user_login_success(user, monkeypatch, cli_runner):
    """Test the user-login command"""
    input_values = iter(['test_admin', 'test_password'])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args,**kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['user-login'])

    assert result.exit_code == 0
    assert 'Your token is' in result.output


def test_user_login_error(user, monkeypatch, cli_runner):
    """Test the user-login command with bad password"""
    input_values = iter(['test_admin', 'wrong_password'])
    monkeypatch.setattr('rich.prompt.PromptBase.ask', lambda *args,**kwargs: next(input_values))

    result = cli_runner.invoke(global_cli, ['user-login'])

    assert result.exit_code == 0
    assert 'Wrong username or password' in result.output
