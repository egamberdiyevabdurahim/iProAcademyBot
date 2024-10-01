from aiogram.fsm.state import StatesGroup, State


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


# PENDING USER
class AddPendingUserState(StatesGroup):
    telegram_id = State()


class DeletePendingUserState(StatesGroup):
    telegram_id = State()


# PANIC ARRAY
class AddPanicArrayState(StatesGroup):
    panic_array_name = State()


class DeletePanicArrayState(StatesGroup):
    panic_array_name = State()


class EditPanicArrayState(StatesGroup):
    panic_array_id = State()
    panic_array_new_name = State()


# PANIC
class AddPanicState(StatesGroup):
    panic_array_id = State()
    panic_name_uz = State()
    panic_name_ru = State()
    panic_name_en = State()
    panic_code = State()


class DeletePanicState(StatesGroup):
    panic_id = State()


# USERSPACE
class AddUserSpaceState(StatesGroup):
    user_space_name_uz = State()
    user_space_name_ru = State()
    user_space_name_en = State()
    user_space_code = State()


class DeleteUserSpaceState(StatesGroup):
    user_space_id = State()


# CHIPSET
class AddChipsetState(StatesGroup):
    chipset_name = State()


class DeleteChipsetState(StatesGroup):
    chipset_id = State()


class EditChipsetState(StatesGroup):
    chipset_id = State()
    chipset_new_name = State()


# I2C Category
class AddI2CCategoryState(StatesGroup):
    category_name = State()


class DeleteI2CCategoryState(StatesGroup):
    category_id = State()


class EditI2CCategoryState(StatesGroup):
    category_id = State()
    category_new_name = State()


# I2C
class AddI2CState(StatesGroup):
    i2c_name_uz = State()
    i2c_name_ru = State()
    i2c_name_en = State()
    chipset_id = State()
    category_id = State()


class DeleteI2CState(StatesGroup):
    i2c_id = State()


# AOP PANIC
class AddAopPanicState(StatesGroup):
    aop_panic_name_uz = State()
    aop_panic_name_ru = State()
    aop_panic_name_en = State()
    aop_panic_code = State()


class DeleteAopPanicState(StatesGroup):
    aop_panic_id = State()


# ALPHABET
class AddAlphabetState(StatesGroup):
    alphabet_name_uz = State()
    alphabet_name_ru = State()
    alphabet_name_en = State()
    alphabet_code = State()


class DeleteAlphabetState(StatesGroup):
    alphabet_id = State()