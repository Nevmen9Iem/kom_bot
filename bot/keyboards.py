# bot/keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def navigation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад"), KeyboardButton(text="На головну")],
            [KeyboardButton(text="Завершити та сформувати рахунок"), KeyboardButton(text="Завершити")]
        ],
        resize_keyboard=True
    )
