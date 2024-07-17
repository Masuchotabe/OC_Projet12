from passlib.hash import argon2

from src.models.user import User, Team
from sqlalchemy.orm import Session

from src.database import engine

def create_user(user_data):
    """Création du user"""

    with Session(engine) as session:

        password_hash = argon2.hash(user_data['password'])
        new_user = User(username=user_data['username'],
                        email=user_data['email'],
                        password=password_hash,
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        phone=user_data.get('phone'),
                        team_id=user_data['team_id']
                        )

        session.add(new_user)
        session.commit()



def get_user(user_id):
    """Retourne un utilsateur à partir de l'id"""
    with Session(engine) as session:
        user = session.query(User).get(user_id)
        return user


def get_users():
    """Retourne tous les utilisateurs"""
    with Session(engine) as session:
        users = session.query(User).all()
        return users


def delete_user(user_id):
    """Suprrime un utilisateur"""
    with Session(engine) as session:
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()


def update_user(user_id, user_data):
    """Met à jour un user en fonction de l'id et des données"""
    with Session(engine) as session:
        user = session.query(User).get(user_id)

        if user_data.get('password'):
            user.password = argon2.hash(user_data.get('password'))
        user.username = user_data.get('username') or user.username
        user.email = user_data.get('email') or user.email
        user.first_name = user_data.get('first_name') or user.first_name
        user.last_name = user_data.get('last_name') or user.last_name
        user.phone = user_data.get('phone') or user.phone
        user.team_id = user_data.get('team_id') or user.team_id

        session.commit()


def create_team(team_data):
    """Création d'une equipe"""
    with Session(engine) as session:
        new_team = Team(name=team_data['name'])
        session.add(new_team)
        session.commit()
        session.refresh(new_team)
