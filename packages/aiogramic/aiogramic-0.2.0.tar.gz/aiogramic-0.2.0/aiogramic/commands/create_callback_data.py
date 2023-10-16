import click
from os.path import abspath

from ..utils.builders import TemplateBuilder
from ..utils.file import write_entity


@click.command("create:callback-data")
@click.argument("callback_data_name")
@click.option("--path", default="src/cbdata")
@click.option("--field", default=tuple(), multiple=True)
@click.option("--prefix", default="")
def create_callback_data(
        callback_data_name: str,
        field: str,
        prefix: str,
        path: str,
):
    destination_path = abspath(path)
    fields = [field.split(":") for field in field]
    builder = TemplateBuilder()
    content = builder.build(
        "callback_data",
        callback_data_name=callback_data_name,
        prefix=prefix,
        fields=fields
    )
    write_entity(
        destination_path,
        filename=f"{callback_data_name.lower()}_cbdata",
        content=content
    )
