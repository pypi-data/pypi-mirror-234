import click

from os.path import abspath


@click.command("create:middleware")
@click.argument("middleware_name")
def create_middleware(
        middleware_name: str
):
    pass
