from aiogram.utils.keyboard import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def example_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    return InlineKeyboardMarkup(
        inline_keyboard=builder.export()
    )
