from aiogram.fsm.state import StatesGroup, State


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
    panic_photo = State()


class DeletePanicState(StatesGroup):
    panic_id = State()


class EditPanicState(StatesGroup):
    panic_id = State()
    panic_new_name_uz = State()
    panic_new_name_ru = State()
    panic_new_name_en = State()
    panic_array_id = State()
    panic_new_code = State()
    panic_new_photo = State()


# USERSPACE
class AddUserSpaceState(StatesGroup):
    user_space_name_uz = State()
    user_space_name_ru = State()
    user_space_name_en = State()
    user_space_code = State()
    user_space_photo = State()


class DeleteUserSpaceState(StatesGroup):
    user_space_id = State()


class EditUserSpaceState(StatesGroup):
    user_space_id = State()
    user_space_new_name_uz = State()
    user_space_new_name_ru = State()
    user_space_new_name_en = State()
    user_space_new_code = State()
    user_space_new_photo = State()


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
    i2c_photo = State()


class DeleteI2CState(StatesGroup):
    i2c_id = State()


class EditI2CState(StatesGroup):
    i2c_id = State()
    i2c_new_name_uz = State()
    i2c_new_name_ru = State()
    i2c_new_name_en = State()
    chipset_id = State()
    category_id = State()
    i2c_new_photo = State()


# AOP PANIC
class AddAopPanicState(StatesGroup):
    aop_panic_name_uz = State()
    aop_panic_name_ru = State()
    aop_panic_name_en = State()
    aop_panic_code = State()
    aop_panic_photo = State()


class DeleteAopPanicState(StatesGroup):
    aop_panic_id = State()


class EditAopPanicState(StatesGroup):
    aop_panic_id = State()
    panic_name_uz = State()
    panic_name_ru = State()
    panic_name_en = State()
    panic_code = State()
    panic_photo = State()


# ALPHABET
class AddAlphabetState(StatesGroup):
    alphabet_name_uz = State()
    alphabet_name_ru = State()
    alphabet_name_en = State()
    alphabet_code = State()
    alphabet_photo = State()


class DeleteAlphabetState(StatesGroup):
    alphabet_id = State()


class EditAlphabetState(StatesGroup):
    alphabet_id = State()
    alphabet_new_name_uz = State()
    alphabet_new_name_ru = State()
    alphabet_new_name_en = State()
    alphabet_new_code = State()
    alphabet_new_photo = State()


# MODEL
class AddModelState(StatesGroup):
    name = State()


class DeleteModelState(StatesGroup):
    model_id = State()


class EditModelState(StatesGroup):
    model_id = State()
    new_name = State()


# SWAP
class AddSwapState(StatesGroup):
    swap_model_id = State()
    swap_title = State()
    swap_name_uz = State()
    swap_name_ru = State()
    swap_name_en = State()
    swap_photos = State()
    end = State()


class DeleteSwapState(StatesGroup):
    swap_id = State()


class EditSwapState(StatesGroup):
    swap_id = State()
    swap_new_model_id = State()
    swap_new_title = State()
    swap_new_name_uz = State()
    swap_new_name_ru = State()
    swap_new_name_en = State()
    swap_photos = State()
    end = State()


# ITUNES
class AddITunesState(StatesGroup):
    itunes_error_code = State()
    itunes_name_uz = State()
    itunes_name_ru = State()
    itunes_name_en = State()
    itunes_photo = State()


class DeleteITunesState(StatesGroup):
    itunes_id = State()


class EditITunesState(StatesGroup):
    itunes_id = State()
    itunes_new_error_code = State()
    itunes_new_name_uz = State()
    itunes_new_name_ru = State()
    itunes_new_name_en = State()
    itunes_new_photo = State()
