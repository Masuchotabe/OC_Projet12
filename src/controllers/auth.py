from passlib.hash import argon2
import jwt
from sqlalchemy.orm import Session

from src.database import engine
from src.models import User
from src.utils import create_token

from src.settings import SECRET_KEY


def user_login(username, password):
    """"""
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if argon2.verify(password, user.password):
            token = create_token(payload_data={"user_id": user.id})
            return token
        else:
            return 'Wrong password'
