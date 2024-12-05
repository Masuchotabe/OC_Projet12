from rich.prompt import Prompt

from views import console


def login_view():
    """
    Prompt the user to enter their username and password to log in.
    Returns:
        tuple: A tuple containing the username and password entered by the user.
        - username (str): The username entered by the user.
        - password (str): The password entered by the user.
    """
    username = Prompt.ask('Username')
    password = Prompt.ask('Password', password=True)
    return username, password

def display_token(token):
    """
    Display the generated token to the user.
    Args:
        token (str): The token to be displayed to the user.
    """
    console.print("Your token is : ")
    console.print(token)
