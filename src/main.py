import click
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.controllers.auth import user_login
from src.controllers.user import *
from src.models import *
from src.utils import get_user_from_token
from database import engine, dump_data

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

# token = user_login('firstuser', 'test_password')
#
# user = get_user_from_token(token)
# # print(user.username)
# user_2 = get_user(token=token, user_id=2)
# print(user_2.username)

dump_data(engine)

# @click.group()
# def cli():
#     click.echo('Welcome to auth')
#
# @click.group()
# def cli2():
#     click.echo('Welcome to auth')
#
#
#
# @cli.command(help='test help 1')
# def command_1():
#     """command 1 for testing"""
#     click.echo('This is command 1')
#
#
# @cli.command()
# def command_2():
#     """command 2 for testing"""
#     click.echo('This is command 2')
#
# @cli2.command(help='test help 1 2')
# def command_2_1():
#     """command 1 for testing"""
#     click.echo('This is command 2')
#
#
# @cli2.command()
# def command_2_2():
#     """command 2 for testing 2"""
#     click.echo('This is command 2')
#
# cli3 = click.CommandCollection(sources=[cli, cli2])
#
# if __name__ == '__main__':
#     cli3()

