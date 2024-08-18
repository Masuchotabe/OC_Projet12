import click
from passlib.hash import argon2

from models import User, Team
from sqlalchemy.orm import Session

from database import engine
from utils import login_required

# @click.group()
# def user_cli(ctx, token):
#     pass

user_cli = click.Group()


@user_cli.command()
@click.argument('token')
@login_required
def create_user(user):
    """Création du user"""
    if not user.has_perm('create_user'):
        return
    user_data = views.prompt_for_user()
    with Session(engine) as session:
        password_hash = argon2.hash(user_data['password'])
        new_user = User(username=user_data.get('username'),
                        personal_number=user_data.get('personal_number'),
                        email=user_data.get('email'),
                        password=password_hash,
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        phone=user_data.get('phone'),
                        team_id=user_data.get('team_id')
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
@login_required
def get_users(user):
    """Retourne tous les utilisateurs"""
    if not user.has_perm('list_users'):
        return
    with Session(engine) as session:
        users = session.query(User).all()
        return users

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
