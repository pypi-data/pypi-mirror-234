import click

from .commands.init_app import init_app
from .commands.create_handler import create_handler
from .commands.create_callback_data import create_callback_data


@click.group()
def cli():
    pass


cli.add_command(init_app)
cli.add_command(create_handler)
cli.add_command(create_callback_data)

if __name__ == "__main__":
    cli()
