import click
from virl.helpers import clear_current_lab


@click.command()
def clear():
    """
    clear the current lab ID
    """

    clear_current_lab()
