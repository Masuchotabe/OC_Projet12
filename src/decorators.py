from functools import wraps

from sqlalchemy.orm import Session

from database import engine
from utils import get_user_from_token


def login_required(func):
    """decorator to ckeck if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.pop("token")
        session = kwargs['session']
        user = get_user_from_token(token, session)
        if user:
            kwargs["user"] = user
            return func(*args, **kwargs)
        else:
            return "You need to login to access this feature"
    return wrapper

def permission_required(permission):
    """decorator to check if user has permission"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if user:
                if not user.has_perm(permission):
                    return "You do not have permission to access this feature"
                else:
                    return func(*args, **kwargs)
        return wrapper
    return decorator

def manage_session(func):
    """decorator to ckeck if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            kwargs['session'] = session  # Passez la session en argument à la fonction
            return func(*args, **kwargs)
    return wrapper