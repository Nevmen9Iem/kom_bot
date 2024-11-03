# bot/states.py

from aiogram.fsm.state import State, StatesGroup

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    ADDRESS_MENU = State()
    SERVICES_MENU = State()
