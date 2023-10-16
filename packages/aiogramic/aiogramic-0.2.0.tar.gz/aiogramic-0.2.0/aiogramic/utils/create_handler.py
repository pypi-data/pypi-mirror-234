from ..utils.builders import TemplateBuilder


def create_message_handler(
        handler_name: str,
        state: bool,
        callback_data_class: str | None,
        callback_data_path: str | None
):
    builder = TemplateBuilder()
    content = builder.build(
        "handlers/message_handler",
        handler_name=handler_name,
        state=state,
        callback_data_class=callback_data_class,
        callback_data_path=callback_data_path
    )
    return content
