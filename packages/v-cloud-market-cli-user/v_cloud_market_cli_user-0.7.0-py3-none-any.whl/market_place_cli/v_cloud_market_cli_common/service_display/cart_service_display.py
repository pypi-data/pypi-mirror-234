from rich.console import Console
from .table import display_table


class CartServiceDisplay:

    def __init__(self, console: Console):
        self.console = console

    def display_cart_table(self, headers: list, status_list: list, justify: str = 'center'):
        self.console.clear()
        title = '[bold bright_magenta] Cart List'
        try:
            w = display_table(self.console, title, headers, status_list, justify, show_lines = True)
            return w
        except Exception as err:
            self.console.print(err)
