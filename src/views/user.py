import time

from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def prompt_for_user(actual_user=None, team_choice=None):
    # console = Console()
    user_data = {}
    user_data['username'] = Prompt.ask('Username')
    user_data['personal_number'] = Prompt.ask('Employee ID')
    user_data['email'] = Prompt.ask('Email')
    user_data['password'] = Prompt.ask('Password', password=True)
    user_data['first_name'] = Prompt.ask('First name')
    user_data['last_name'] = Prompt.ask('Last name')
    user_data['phone'] = Prompt.ask('Phone')
    user_data['team_name'] = Prompt.ask('Team name', choices=['Sales team','Support team','Management team'])
    return user_data

def display_users(users):
    table = Table(title='Users' ,header_style="bold magenta")
    table.add_column('Id')
    table.add_column('Employee ID')
    table.add_column('Email')
    table.add_column('First name')
    table.add_column('Last name')
    table.add_column('Phone')
    table.add_column('Team')
    for user in users:
        table.add_row(str(user.id), user.personal_number, user.email,
                      user.first_name, user.last_name, user.phone, str(user.team))
    console.print(table)
