from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.controllers.user import create_team
from src.models.user import *
from src.models.customer import *


# engine = create_engine("sqlite://", echo=True)
from src.models import create_all, create_engine

# create_all()

create_team({'name': 'first team'})

create_user({'username': 'firstuser', 'email': 'firstuser@test.com', 'password': 'test_password'})