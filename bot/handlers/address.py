# bot/handlers/address.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import navigation_keyboard
from bot.utils.db import save_address, get_addresses
from bot.states import MenuStates

router = Router()

# Обробник для кнопки "Додати адресу"
@router.message(lambda message: message.text == "Додати адресу")
async def add_address(message: types.Message, state: FSMContext):
    # Показуємо кнопки з типами житла
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Квартира")],
            [KeyboardButton(text="Приватний будинок")],
            [KeyboardButton(text="Назад"), KeyboardButton(text="На головну")]
        ],
        resize_keyboard=True
    )
    await message.answer("Виберіть вид житла:", reply_markup=markup)
    await state.set_state(MenuStates.ADDRESS_MENU)

# Обробник для вибору "Квартира"
@router.message(lambda message: message.text == "Квартира")
async def apartment_address(message: types.Message, state: FSMContext):
    await message.answer("Введіть місто:", reply_markup=navigation_keyboard())
    await state.update_data(housing_type="Квартира")
    await state.set_state("CITY")

# Обробник для вибору "Приватний будинок"
@router.message(lambda message: message.text == "Приватний будинок")
async def private_house_address(message: types.Message, state: FSMContext):
    await message.answer("Введіть місто:", reply_markup=navigation_keyboard())
    await state.update_data(housing_type="Приватний будинок")
    await state.set_state("CITY")

# Обробник для введення міста
@router.message(StateFilter("CITY"))
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введіть вулицю:", reply_markup=navigation_keyboard())
    await state.set_state("STREET")

# Обробник для введення вулиці
@router.message(StateFilter("STREET"))
async def process_street(message: types.Message, state: FSMContext):
    await state.update_data(street=message.text)
    await message.answer("Введіть номер будинку:", reply_markup=navigation_keyboard())
    await state.set_state("HOUSE_NUMBER")

# Обробник для введення номеру будинку
@router.message(StateFilter("HOUSE_NUMBER"))
async def process_house_number(message: types.Message, state: FSMContext):
    await state.update_data(house_number=message.text)
    data = await state.get_data()

    if data.get("housing_type") == "Квартира":
        await message.answer("Введіть номер під'їзду:", reply_markup=navigation_keyboard())
        await state.set_state("ENTRANCE")
    else:
        save_address(data)  # Зберігаємо адресу для приватного будинку
        await message.answer("Адресу збережено! Повернення до головного меню.", reply_markup=navigation_keyboard())
        await state.clear()  # Очищаємо стан для завершення процесу
        await send_main_menu(message)  # Повернення до головного меню

# Обробник для введення номеру під'їзду
@router.message(StateFilter("ENTRANCE"))
async def process_entrance(message: types.Message, state: FSMContext):
    await state.update_data(entrance=message.text)
    await message.answer("Адресу збережено! Повернення до головного меню.", reply_markup=navigation_keyboard())
    save_address(await state.get_data())  # Зберігаємо повну адресу для квартири
    await state.clear()  # Очищаємо стан для завершення процесу
    await send_main_menu(message)  # Повернення до головного меню

# Відображення головного меню після завершення створення адреси
async def send_main_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вибрати адресу")],
            [KeyboardButton(text="Додати адресу")]
        ],
        resize_keyboard=True
    )
    await message.answer("Ви в головному меню. Виберіть дію:", reply_markup=markup)
