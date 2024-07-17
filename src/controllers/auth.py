from passlib.hash import argon2
import jwt
from sqlalchemy.orm import Session

from src.database import engine
from src.models import User


my_secret = 'my_super_secret'


def user_login(username, password):
    """"""
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if argon2.verify(password, user.password):
            payload_data = {
                "user_id": user.id,
                "username": user.username
            }
            token = jwt.encode(payload=payload_data, key=my_secret)
            return token
        else:
            return 'Wrong password'
