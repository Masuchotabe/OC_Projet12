import click
import sentry_sdk

from controllers.auth import auth_cli
from controllers.contract import contract_cli
from controllers.customer import customer_cli
from controllers.event import event_cli
from controllers.user import user_cli
from database import config_group


global_cli = click.CommandCollection(name='test', sources=[auth_cli, user_cli, customer_cli, event_cli, contract_cli, config_group])

if __name__ == '__main__':
    global_cli()
    sentry_sdk.flush()


