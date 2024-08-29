import click
from click import pass_context
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from controllers.auth import auth_cli, user_login
from controllers.contract import contract_cli
from controllers.customer import customer_cli
from controllers.event import event_cli
from controllers.user import user_cli, create_user
from database import config_group

# from controllers.auth import user_login
# from controllers.user import *
# from models import *
# from utils import get_user_from_token
# from database import engine, dump_data, load_data

# engine = create_engine("sqlite://", echo=True)
# from models import create_all, create_engine

# create_all()

# create_team({'name': 'Sales team'})
# create_team({'name': 'Support team'})
# create_team({'name': 'Management team'})

# create_user({
#     'username': 'amanager',
#     'email': 'amanager@test.com',
#     'password': 'amanager_password',
#     'personal_number': '0123456789',
#     'team_id': 3,
# })

# update_user(user_id=1, user_data={
#     'first_name': 'prenom'
# })
#
# token = user_login('amanager', 'amanager_password')
# print(token)
# #
# user = get_user_from_token(token)
# print(user.username)
# user_2 = get_user(token=token, user_id=2)
# print(user_2.username)

# dump_data(engine, 'fixtures/init_data.json')

# load_data(engine)

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
# #
global_cli = click.CommandCollection(name='test', sources=[auth_cli, user_cli, customer_cli, event_cli, contract_cli, config_group])

# global_v2 = click.Group('global')
# global_v2.add_command(global_cli)
# global_v2.add_command(config_group)



# # @click.CommandCollection(sources=[auth_cli, user_cli, customer_cli, event_cli, contract_cli])
# # @click.argument('token')
# # @pass_context
# # def global_cli(ctx, token):
# #     click.echo(f'{token=}')
#
if __name__ == '__main__':
    global_cli()

