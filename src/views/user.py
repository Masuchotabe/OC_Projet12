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
    headers = ['Id', 'Employee ID', 'Username', 'Email', 'First name', 'Last name', 'Phone', 'Team']
    title = "Users" if len(users) >1 else "User"
    rows = []
    for user in users:
        rows.append((user.id, user.personal_number,user.username, user.email,
                      user.first_name, user.last_name, user.phone, user.team))
    display_table(headers, rows, title)

def display_table(headers, rows, title):
    table = Table(title=title)
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*[str(e) if e else e for e in row])
    console.print(table)

