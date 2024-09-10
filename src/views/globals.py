from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

def display_table(headers, rows, title):
    table = Table(title=title)
    for header in headers:
        table.add_column(header)
    for row in rows:
        table.add_row(*[str(e) if e else e for e in row])
    console.print(table)


def ask_for(message, password=False):
    message = message + r" [dark_magenta]\[Enter \q to exit]"
    val = Prompt.ask(message, password=password)
    return val, val.strip() == r'\q'


def ask_confirm(message):
    return Confirm.ask(message, default=True)


def show_error(error_message):
    console.print(error_message, style="red")
