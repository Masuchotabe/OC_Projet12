import os
from datetime import timedelta, datetime, timezone
from functools import wraps

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from models import User
from settings import SECRET_KEY


def get_user_from_token(token, session):
    """
    Return the user connected with jwt_token, else return None
    Args:
        token(str):
        session(Session):

    Returns(User):
    """
    print(token)
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print('token is expired')
        return None
    except jwt.InvalidTokenError:
        print('token is invalid')
        return None

    user_id = payload.get("user_id")
    user = session.scalar(select(User).where(User.id == user_id))
    return user


def create_token(payload_data):
    """Create a JWT token with the given payload_data dict"""
    expiration_date = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    payload_data.update({"exp": expiration_date})
    return jwt.encode(payload=payload_data, key=SECRET_KEY)


