import click

from .commands.init_app import init_app
from .commands.create_handler import create_handler


@click.group()
def cli():
    pass


cli.add_command(init_app)
cli.add_command(create_handler)

if __name__ == "__main__":
    cli()
