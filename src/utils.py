import os
from datetime import timedelta, datetime, timezone
from functools import wraps

import jwt
from sqlalchemy.orm import Session

import settings
from database import engine
from models import User
from settings import SECRET_KEY


def get_user_from_token(token):
    """Return the user connected with jwt_token, else return None"""
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
    with Session(engine) as session:
        user = session.query(User).get(user_id)
    return user


def create_token(payload_data):
    """Create a JWT token with the given payload_data dict"""
    expiration_date = datetime.now(tz=timezone.utc) + timedelta(hours=1)
    payload_data.update({"exp": expiration_date})
    return jwt.encode(payload=payload_data, key=SECRET_KEY)


def login_required(func):
    """decorator to ckeck if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.pop("token")
        user = get_user_from_token(token)
        if user:
            kwargs["user"] = user
            return func(*args, **kwargs)
        else:
            return "You need to login to access this feature"
    return wrapper
