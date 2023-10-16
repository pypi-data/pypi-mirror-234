from aiogram import Bot
from aiogram import Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from aiohttp.web import Application
from aiohttp.web import run_app

from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.webhook.aiohttp_server import setup_application

from .cfg import AppConfig


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=f"{AppConfig.base_url}{AppConfig.webhook_path}"
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def main() -> None:
    app = Application()

    storage = MemoryStorage()

    bot = Bot(token=AppConfig.telegram_token)

    dispatcher = Dispatcher(storage=storage, bot=bot)

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    SimpleRequestHandler(
        bot=bot,
        dispatcher=dispatcher
    ).register(
        app,
        path=AppConfig.webhook_path
    )

    setup_application(app, dispatcher)

    run_app(app, host=AppConfig.app_host, port=AppConfig.app_port)


if __name__ == "__main__":
    main()
