# bot/routers.py

from aiogram import Dispatcher
from bot.handlers.start import router as start_router
from bot.handlers.address import router as address_router
from bot.handlers.services import router as services_router

def register_all_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(address_router)
    dp.include_router(services_router)
