# bot/handlers/start.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import navigation_keyboard
from bot.utils.db import get_addresses, get_measurements_by_address  # Імпорт функції get_addresses
from bot.states import MenuStates  # Імпортуємо MenuStates

router = Router()

# Головне меню
@router.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вибрати адресу")],
            [KeyboardButton(text="Додати адресу")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привіт! Виберіть адресу або додайте нову.", reply_markup=markup)
    await state.set_state(MenuStates.MAIN_MENU)

# Меню вибору адреси
@router.message(lambda message: message.text == "Вибрати адресу")
async def choose_address(message: types.Message, state: FSMContext):
    addresses = get_addresses()  # Отримуємо адреси з бази даних
    if not addresses:
        await message.answer("Немає збережених адрес. Додайте нову адресу.")
        return

    address_buttons = [[KeyboardButton(text=address)] for address in addresses]
    markup = ReplyKeyboardMarkup(keyboard=address_buttons, resize_keyboard=True)
    await message.answer("Оберіть адресу зі списку:", reply_markup=markup)
    await state.set_state(MenuStates.ADDRESS_MENU)

# Обробник для вибору адреси і переходу до меню послуг
@router.message(lambda message: message.text in get_addresses())
async def handle_selected_address(message: types.Message, state: FSMContext):
    await show_services_menu(message)
    await state.set_state(MenuStates.SERVICES_MENU)  # Змінюємо стан на меню послуг

# Функція для відображення меню з послугами
async def show_services_menu(message: types.Message):
    services_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Електроенергія"), KeyboardButton(text="Газ")],
            [KeyboardButton(text="Доставка газу"), KeyboardButton(text="Опалення")],
            [KeyboardButton(text="Обслуговування котельні"), KeyboardButton(text="Вода та водовідведення")],
            [KeyboardButton(text="Управління будинком"), KeyboardButton(text="Охорона")],
            [KeyboardButton(text="Домофон"), KeyboardButton(text="Інтернет")],
            [KeyboardButton(text="Інше"), KeyboardButton(text="Закінчити та сформувати рахунок")],
            [KeyboardButton(text="Назад"), KeyboardButton(text="На головну")]
        ],
        resize_keyboard=True
    )
    await message.answer("Зробіть вибір послуги:", reply_markup=services_keyboard)

# Обробник для кнопки "На головну"
@router.message(lambda message: message.text == "На головну")
async def go_to_main_menu(message: types.Message, state: FSMContext):
    main_menu_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Вибрати адресу")],
            [KeyboardButton(text="Додати адресу")]
        ],
        resize_keyboard=True
    )
    await message.answer("Повернення до головного меню.", reply_markup=main_menu_keyboard)
    await state.set_state(MenuStates.MAIN_MENU)

# Обробник для кнопки "Сформувати рахунок"
@router.message(lambda message: message.text == "Сформувати рахунок")
async def generate_bill(message: types.Message, state: FSMContext):
    data = await state.get_data()
    address_id = data.get("address_id")
    measurements = get_measurements_by_address(address_id)

    if not measurements:
        await message.answer("Для цієї адреси немає жодних показників.")
        return

    # Формування рахунку
    bill_text = "Рахунок за адресою:\n"
    for service, previous, current, amount, date in measurements:
        bill_text += f"{service} ({date}): {previous} - {current} = {amount:.2f} грн\n"

    await message.answer(bill_text)
