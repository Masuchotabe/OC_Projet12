from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.controllers.auth import user_login
from src.controllers.user import *
from src.models import *



# engine = create_engine("sqlite://", echo=True)
# from src.models import create_all, create_engine

# create_all()

# create_team({'name': 'first team'})

# create_user({
#     'username': 'second_user',
#     'email': 'second_user@test.com',
#     'password': 'test_password',
#     'team_id': 1,
# })

# update_user(user_id=1, user_data={
#     'first_name': 'prenom'
# })

token = user_login('firstuser', 'test_password')
