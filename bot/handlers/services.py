# bot/handlers/services.py

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import navigation_keyboard
from bot.utils.db import save_measurement, get_measurements_by_address, get_addresses
from bot.states import MenuStates

router = Router()

# Обробник для вибору "Електроенергія"
@router.message(lambda message: message.text == "Електроенергія")
async def electricity_service(message: types.Message, state: FSMContext):
    meter_type_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Однозонний")],
            [KeyboardButton(text="Двозонний")],
            [KeyboardButton(text="Трьохзонний")],
            [KeyboardButton(text="Назад"), KeyboardButton(text="На головну")]
        ],
        resize_keyboard=True
    )
    await message.answer("Оберіть тип лічильника:", reply_markup=meter_type_keyboard)
    await state.set_state("ELECTRICITY_METER_TYPE")

@router.message(StateFilter("ELECTRICITY_SINGLE_CURRENT"))
async def electricity_single_current_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        previous = float(data.get("electricity_previous"))
        current = float(message.text)
        amount = (current - previous) * 4.32
        await message.answer(f"Вартість за спожиту електроенергію: {amount:.2f} грн")

        # Збереження показників у базу
        address_id = data.get("address_id")
        save_measurement(address_id, "Електроенергія", previous, current, amount)
    except ValueError:
        await message.answer("Введені значення мають бути числовими. Спробуйте ще раз.")
    await state.clear()


# Обробники для типу "Двозонний"
@router.message(StateFilter("ELECTRICITY_DOUBLE_NIGHT_PREVIOUS"))
async def electricity_double_night_previous_input(message: types.Message, state: FSMContext):
    await state.update_data(double_night_previous=message.text)
    await message.answer("Введіть поточні показники електроенергії в зоні Ніч:")
    await state.set_state("ELECTRICITY_DOUBLE_NIGHT_CURRENT")

@router.message(StateFilter("ELECTRICITY_DOUBLE_NIGHT_CURRENT"))
async def electricity_double_night_current_input(message: types.Message, state: FSMContext):
    await state.update_data(double_night_current=message.text)
    await message.answer("Введіть попередні показники електроенергії в зоні День:")
    await state.set_state("ELECTRICITY_DOUBLE_DAY_PREVIOUS")

@router.message(StateFilter("ELECTRICITY_DOUBLE_DAY_PREVIOUS"))
async def electricity_double_day_previous_input(message: types.Message, state: FSMContext):
    await state.update_data(double_day_previous=message.text)
    await message.answer("Введіть поточні показники електроенергії в зоні День:")
    await state.set_state("ELECTRICITY_DOUBLE_DAY_CURRENT")

@router.message(StateFilter("ELECTRICITY_DOUBLE_DAY_CURRENT"))
async def electricity_double_day_current_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        night_previous = float(data.get("double_night_previous"))
        night_current = float(data.get("double_night_current"))
        day_previous = float(data.get("double_day_previous"))
        day_current = float(message.text)

        night_cost = (night_current - night_previous) * 4.32 * 0.5
        day_cost = (day_current - day_previous) * 4.32
        total_cost = night_cost + day_cost

        await message.answer(f"Вартість за спожиту електроенергію: {total_cost:.2f} грн")
    except ValueError:
        await message.answer("Введені значення мають бути числовими. Спробуйте ще раз.")
    await state.clear()

# Обробник для вибору "Газ"
@router.message(lambda message: message.text == "Газ")
async def gas_service(message: types.Message, state: FSMContext):
    await message.answer("Введіть попередні показники газу:", reply_markup=navigation_keyboard())
    await state.set_state("GAS_PREVIOUS")

@router.message(StateFilter("GAS_PREVIOUS"))
async def gas_previous_input(message: types.Message, state: FSMContext):
    await state.update_data(gas_previous=message.text)
    await message.answer("Введіть останні показники газу:")
    await state.set_state("GAS_CURRENT")

@router.message(StateFilter("GAS_CURRENT"))
async def gas_current_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        previous = float(data.get("gas_previous"))
        current = float(message.text)
        cost = (current - previous) * 8.00  # Приклад: змінюйте за потреби
        await message.answer(f"Вартість за спожитий газ: {cost:.2f} грн")
    except ValueError:
        await message.answer("Введені значення мають бути числовими. Спробуйте ще раз.")
    await state.clear()

# Додайте аналогічні обробники для інших послуг, як-от "Вода та водовідведення", "Опалення" тощо
