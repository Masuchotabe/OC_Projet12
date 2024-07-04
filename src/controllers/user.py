from passlib.hash import argon2

from src.models.user import User, Team
from sqlalchemy.orm import Session

from src.database import engine


def create_user(user_data):
    """Création du user"""
    with Session(engine) as session:

        password_hash = argon2.hash(user_data['password'])
        new_user = User(username=user_data.get('username'),
                        email=user_data.get('email'),
                        password=password_hash,
                        first_name=user_data.get('first_name'),
                        last_name=user_data.get('last_name'),
                        phone=user_data.get('phone'),
                        team_id=user_data.get('team_id')
                        )

        session.add(new_user)


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
