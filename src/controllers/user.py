import click
from passlib.hash import argon2
from sqlalchemy import select, Select

from views.user import prompt_for_user, display_users, ask_for, show_error
from models import User, Team
from sqlalchemy.orm import Session

from database import engine
from decorators import login_required, permission_required, manage_session

user_cli = click.Group()

@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('create_user')
def create_user(user, session):
    """
    Création du user
    Args:
        user(User): user connecté via le token
        session(Session): session sqlalchemy
    """
    teams_name = session.scalars(select(Team.name)).all()

    user_data = prompt_for_user(team_choice=teams_name)
    team = session.scalars(
        select(Team).where(Team.name==user_data.get('team_name'))
    ).first()
    password_hash = argon2.hash(user_data['password'])

    new_user = User(username=user_data.get('username'),
                    personal_number=user_data.get('personal_number'),
                    email=user_data.get('email'),
                    password=password_hash,
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    phone=user_data.get('phone'),
                    team=team
                    )
    session.add(new_user)
    session.commit()

@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('read_user')
def get_user(user, session):
    """Voir le détail d'un utilisateur"""
    is_valid = False
    target_user = None
    while not is_valid:
        target_username, stop = ask_for('Enter the username of the user')
        if stop:
            break
        target_user = session.execute(Select(User).filter_by(username=target_username)).scalar()
        if target_user:
            is_valid = True
        else:
            show_error('Wrong username, try again.')

    if target_user:
        display_users([target_user])

@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('list_users')
def get_users(user, session):
    """Retourne tous les utilisateurs
    Args:
        user(User): user connecté via la token
        session(Session): session sqlalchemy
    """
    users = session.scalars(select(User)).all()
    display_users(users)


@user_cli.command()
@click.argument('token')
@login_required
def delete_user(user_id, user):
    """Supprime un utilisateur"""
    if not user.has_perm('delete_users'):
        return
    with Session(engine) as session:
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()

@user_cli.command()
@click.argument('token')
@manage_session
@login_required
@permission_required('update_user')
def update_user(user, session):
    """Met à jour un user en fonction de l'id et des données"""
    is_valid = False
    target_user = None
    while not is_valid:
        target_username, stop = ask_for('Enter the username of the user')
        if stop:
            break
        target_user = session.execute(Select(User).filter_by(username=target_username)).scalar()
        if target_user:
            is_valid = True
        else:
            show_error('Wrong username, try again.')

    if not target_user:
        return

    teams_name = session.scalars(select(Team.name)).all()
    user_data = prompt_for_user(actual_user=target_user, team_choice=teams_name)
    team = session.scalars(
        select(Team).where(Team.name == user_data.get('team_name'))
    ).first()
    if user_data['password']:
        user_data['password'] = argon2.hash(user_data['password'])
    for key, value in user_data.items():
        setattr(target_user, key, value)
    session.commit()


def create_team(team_data):
    """Création d'une equipe"""
    with Session(engine) as session:
        new_team = Team(name=team_data['name'])
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
