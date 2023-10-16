from aiogram import Router

# Routers
from .command.router import router as command_router

router = Router()

router.include_router(command_router)
