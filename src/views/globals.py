from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table

console = Console()

def display_table(headers, rows, title):
    """
    Display a tabular representation of data.
    Args:
        headers (list): A list of column headers for the table.
        rows (list of tuples): The data to be displayed, where each tuple represents a row.
        title (str): The title of the table.
    """
    table = Table(title=title)
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*[str(e) if e is not None else e for e in row])
    console.print(table)


def ask_for(message, password=False, output_type=str):
    """
   Prompt the user for input with flexible type and options.
   Args:
       message (str): The message to display to the user.
       password (bool, optional): If True, input will be hidden (default: False).
       output_type (type, optional): The type of the expected input. Supported types:
           - `str`: A string (default).
           - `int`: An integer.
           - `bool`: A boolean value (yes/no confirmation).
           - `float`: A floating-point number.
   Returns:
       str, int, bool, or float: The user's input, converted to the specified type.
   """
    if output_type == str:
        val = Prompt.ask(message, password=password)
    elif output_type == int:
        val = IntPrompt.ask(message, password=password)
    elif output_type == bool:
        val = Confirm.ask(message, default=True)
    elif output_type == float:
        val = FloatPrompt.ask(message, password=password)
    else:
        raise ValueError(f"Invalid output type: {output_type}")
    return val


def show_error(error_message):
    """
    Display an error message in red.
    Args:
        error_message (str): The error message to display.
    """
    console.print(error_message, style="red")


def show_success(message):
    """
    Display a success/confirmation message in green.
    Args:
        message (str): The message to display.
    """
    console.print(message, style="green")
