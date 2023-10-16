import click

from ..enums import EntityType
from ..utils.create_handler import create_message_handler


@click.command("create")
@click.argument("entity_type")
@click.argument("handler_name")
@click.option("--state", "-s", is_flag=True)
@click.option("--callback-data")
def create_handler(
        entity_type: EntityType,
        handler_name: str,
        state: bool,
        callback_data: str
):
    print(entity_type)

    match entity_type:
        case EntityType.HANDLER:
            pass
        case EntityType.CALLBACK_DATA:
            pass
        case EntityType.KEYBOARD:
            pass
        case EntityType.STATE:
            pass
        case EntityType.MIDDLEWARE:
            pass
        case _:
            print(EntityType)

    if callback_data:
        callback_data_path = callback_data.split(".")
        callback_data_class = callback_data_path[-1]
        callback_data_path.pop()
        callback_data_path = ".".join(callback_data_path)
    else:
        callback_data_class = None
        callback_data_path = None

    create_message_handler(
        handler_name,
        state=state,
        callback_data_class=callback_data_class,
        callback_data_path=callback_data_path
    )
