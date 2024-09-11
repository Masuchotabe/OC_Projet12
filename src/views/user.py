from rich.prompt import Prompt

from .globals import display_table


def prompt_for_user(actual_user=None, team_choice=None):
    user_data = {}
    if actual_user:
        user_data['username'] = Prompt.ask('Username', default=actual_user.username)
        user_data['personal_number'] = Prompt.ask('Employee ID', default=actual_user.personal_number)
        user_data['email'] = Prompt.ask('Email', default=actual_user.email)
        user_data['password'] = Prompt.ask('Password', password=True)
        user_data['first_name'] = Prompt.ask('First name', default=actual_user.first_name)
        user_data['last_name'] = Prompt.ask('Last name', default=actual_user.last_name)
        user_data['phone'] = Prompt.ask('Phone', default=actual_user.phone)
        user_data['team_name'] = Prompt.ask('Team name', choices=team_choice, default=str(actual_user.team))
    else:
        user_data['username'] = Prompt.ask('Username')
        user_data['personal_number'] = Prompt.ask('Employee ID')
        user_data['email'] = Prompt.ask('Email')
        user_data['password'] = Prompt.ask('Password', password=True)
        user_data['first_name'] = Prompt.ask('First name')
        user_data['last_name'] = Prompt.ask('Last name')
        user_data['phone'] = Prompt.ask('Phone')
        if team_choice:
            user_data['team_name'] = Prompt.ask('Team name', choices=team_choice)
    return user_data

def display_users(users):
    headers = ['Id', 'Employee ID', 'Username', 'Email', 'First name', 'Last name', 'Phone', 'Team']
    title = "Users" if len(users) >1 else "User"
    rows = []
    for user in users:
        rows.append((user.id, user.personal_number,user.username, user.email,
                      user.first_name, user.last_name, user.phone, user.team))
    display_table(headers, rows, title)

