import click
from passlib.hash import argon2
from sqlalchemy import select

from views.user import prompt_for_user, display_users
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
        user(User): user connecté via la token
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
@login_required
def get_user(user_id, user):
    """Retourne un utilsateur à partir de l'id"""
    if not user.has_perm('read_user'):
        return
    with Session(engine) as session:
        user = session.query(User).get(user_id)
        return user

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
@login_required
def update_user(user_id, user_data, user):
    """Met à jour un user en fonction de l'id et des données"""
    if not user.has_perm('update_users'):
        return
    with Session(engine) as session:
        user = session.query(User).get(user_id)

        for key, value in user_data.items():
            setattr(user, key, value)
        session.commit()


def create_team(team_data):
    """Création d'une equipe"""
    with Session(engine) as session:
        new_team = Team(name=team_data['name'])
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
