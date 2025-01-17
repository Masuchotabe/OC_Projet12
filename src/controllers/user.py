import click


from views import prompt_for_user, display_users, ask_for, show_error
from models import User, Team
from sqlalchemy.orm import Session

from decorators import login_required, permission_required, manage_session

user_cli = click.Group()

@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_user')
def create_user(user, session):
    """
    Create a new user.
    Args:
        user(User): Connected user from token.
        session(Session): SQLAlchemy session.
    """
    teams_name = [team.name for team in Team.get_teams(session)]
    user_data = ask_for_user_data(session=session, teams_name=teams_name)

    if user_data:
        User.create(session, user_data)


@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('read_user')
def get_user(user, session):
    """
    Retrieve details of a specific user.
    Args:
        user(User): Connected user from the token.
        session(Session): SQLAlchemy session.
    """
    target_user = ask_for_user(session)

    if target_user:
        display_users([target_user])


@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_users')
def get_users(user, session):
    """
    Retrieve a list of all users.
    Args:
        user(User): Connected user from the token.
        session(Session): SQLAlchemy session.
    """
    users = User.get_users(session)
    display_users(users)


@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('delete_users')
def delete_user(user, session):
    """
    Delete a user based on their username.
    Args:
        user(User): Connected user from the token.
        session(Session): SQLAlchemy session.
    """
    is_valid = False
    target_user = None
    while not is_valid:
        target_username, stop = ask_for('Enter the username of the user')
        if stop:
            break
        target_user = User.get_user(session, username=target_username)
        if target_user:
            is_valid = True
        else:
            show_error('Wrong username, try again.')

    if target_user:
        target_user.delete(session)


@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_user')
def update_user(user, session):
    """
    Update a user based on their ID and provided data.
    Args:
        user(User): Connected user from the token.
        session(Session): SQLAlchemy session.
    """
    target_user = ask_for_user(session)
    if not target_user:
        return

    teams_name = [team.name for team in Team.get_teams(session)]
    user_data = ask_for_user_data(session, target_user, teams_name)

    if user_data:
        target_user.update(session, user_data)


@user_cli.command()
@manage_session
def create_admin(session):
    """
    Create an admin user. Only allowed if the database is empty.
    Args:
        session(Session): SQLAlchemy session.
    """
    if User.get_users(session):
        show_error("Initialization failed: Users already exist in the database. This feature is only available for an empty database.")
        return

    try_again = True
    user_data = dict()
    while try_again:
        user_data = prompt_for_user()
        errors = User.validate_data(user_data)
        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_for('Try again ?', output_type=bool)

    if user_data:
        user_data['team'] = Team.get_team(session, "Management team")
        User.create(session, user_data)


def ask_for_user(session):
    """
    Prompt to select a user by their username.
    Args:
        session(Session): SQLAlchemy session.
    Returns:
        User or None: The selected user or None if canceled.
    """
    try_again = True
    target_user = None
    while try_again:
        target_username = ask_for('Enter the username of the user')
        if target_username:
            target_user = User.get_user(session, username=target_username)
            if target_user:
                break
            else:
                show_error('Wrong username.')
        try_again = ask_for('Try again ?', output_type=bool)
    return target_user


def ask_for_user_data(session, user=None, teams_name=None):
    """
    Prompt for user data for creation or update.
    Args:
        session(Session): SQLAlchemy session.
        user(User, optional): Existing user to update. Defaults to None.
        teams_name(list): List of team names for selection.
    Returns:
        dict or None: User data dictionary or None if canceled.
    """
    try_again = True
    user_data = dict()
    while try_again:
        user_data = prompt_for_user(actual_user=user, team_choice=teams_name)
        if user and not user_data['password']:  # Remove password field if empty during update
            user_data.pop('password')
        errors = User.validate_data(user_data)
        if user_data['team_name'] and not Team.get_team(session, user_data['team_name']):
            errors.append('Wrong team name')
        elif user_data['team_name']:
            user_data['team'] = Team.get_team(session, user_data['team_name'])
        if not errors:
            break
        for error in errors:
            show_error(error)
        try_again = ask_for('Try again ?', output_type=bool)

    return user_data if try_again else None
