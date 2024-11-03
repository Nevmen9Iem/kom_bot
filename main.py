import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.routers import register_all_routers
from bot.utils.db import initialize_db

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if API_TOKEN is None:
    raise ValueError("API_TOKEN не завантажено. Перевірте файл .env і правильність змінної API_TOKEN")

initialize_db()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def clear_commands(bot: Bot):
    await bot.set_my_commands([])  # Очищаємо головне меню команд

async def main():
    # Реєструємо всі обробники через функцію register_all_routers
    register_all_routers(dp)

    # Запуск полінгу
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
