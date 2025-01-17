from functools import wraps

from sentry_sdk import set_user
from sqlalchemy.orm import Session

from database import get_engine
from utils import get_user_from_token
from views import show_error


def manage_session(func):
    """Intègre une session s'il n'y en pas déjà."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get("session"):
            return func(*args, **kwargs)
        engine = get_engine()
        with Session(engine) as session:
            kwargs['session'] = session
            return func(*args, **kwargs)
    return wrapper


def login_required(func):
    """decorator to ckeck if user is logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.pop("token")
        session = kwargs['session']
        user = get_user_from_token(token, session)
        if user:
            kwargs["user"] = user
            set_user({"username": user.username})
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
                    show_error("You do not have permission to access this feature")
                else:
                    return func(*args, **kwargs)
        return wrapper
    return decorator
