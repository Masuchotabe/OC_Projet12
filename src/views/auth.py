from rich.prompt import Prompt

from views import console


def login_view():
    """Affiche la connexion utilisateur"""
    username = Prompt.ask('Username')
    password = Prompt.ask('Password', password=True)
    return username, password

def display_token(token):
    """Affiche le token"""
    console.print("Your token is : ")
    console.print(token)
