from aiogram.fsm.state import StatesGroup, State


class AddAdminState(StatesGroup):
    id_of = State()
    confirm = State()


class DeleteAdminState(StatesGroup):
    id_of = State()
    confirm = State()


# USER
class AddUserState(StatesGroup):
    telegram_id = State()


class DeleteUserState(StatesGroup):
    telegram_id = State()


class ShowActivityState(StatesGroup):
    user_id = State()


class ActivateUserState(StatesGroup):
    user_id = State()
    starts_at = State()
    ends_at = State()
    duration = State()


class ScheduleActivateUser(StatesGroup):
    user_id = State()
    duration = State()


class InActivateUserState(StatesGroup):
    user_id = State()


class SendMessageState(StatesGroup):
    send = State()