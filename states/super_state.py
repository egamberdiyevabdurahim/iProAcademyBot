from aiogram.fsm.state import StatesGroup, State


class AddAdminState(StatesGroup):
    id_of = State()
    confirm = State()


class DeleteAdminState(StatesGroup):
    id_of = State()
    confirm = State()