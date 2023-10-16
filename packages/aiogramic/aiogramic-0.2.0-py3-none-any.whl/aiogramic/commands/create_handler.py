import click

from os.path import abspath

from ..utils.create_handler import create_message_handler
from ..utils.file import write_entity


@click.command("create:handler")
@click.argument("handler_name")
@click.option("--state", "-s", is_flag=True)
@click.option("--callback-data")
@click.option("--path", "-p", default="src/handlers")
def create_handler(
        handler_name: str,
        state: bool,
        callback_data: str,
        path: str
):
    destination_path = abspath(path)
    if callback_data:
        callback_data_path = callback_data.split(".")
        callback_data_class = callback_data_path[-1]
        callback_data_path.pop()
        callback_data_path = ".".join(callback_data_path)
    else:
        callback_data_class = None
        callback_data_path = None

    content = create_message_handler(
        handler_name,
        state=state,
        callback_data_class=callback_data_class,
        callback_data_path=callback_data_path
    )

    write_entity(
        destination_path,
        filename=f"{handler_name}",
        content=content
    )
