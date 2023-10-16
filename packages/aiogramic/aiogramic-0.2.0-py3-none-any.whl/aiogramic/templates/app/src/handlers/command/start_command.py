from aiogram.types import Message
from aiogram.filters.command import CommandObject


async def start_command(
        message: Message,
        command: CommandObject
) -> None:
    await message.answer("Example text")
