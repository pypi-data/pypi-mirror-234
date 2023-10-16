from aiogram import Router
from aiogram.filters.command import CommandStart

# Handlers
from .start_command import start_command

router = Router()

router.message.register(
    start_command,
    CommandStart()
)
