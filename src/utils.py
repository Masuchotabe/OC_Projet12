import os
from functools import wraps

import jwt
from sqlalchemy.orm import Session

from src import settings
from src.database import engine
from src.models import User
from src.settings import SECRET_KEY


def get_connected_user(token):
    """Return the user connected with jwt_token, else return None"""
    if not token:
        return None
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    user_id = payload.get("user_id")
    with Session(engine) as session:
        user = session.query(User).get(user_id)
    return user


def login_required(func):
    """decorator to ckeck if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_user_from_token()
