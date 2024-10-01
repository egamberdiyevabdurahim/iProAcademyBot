from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    first_name = State()
    last_name = State()
    telegram_id = State()
    language_code = State()
    phone_number = State()
