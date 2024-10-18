from aiogram.fsm.state import StatesGroup, State


class PanicState(StatesGroup):
    to_array = State()
    after_array = State()


class UserSpaceState(StatesGroup):
    to_data = State()


class AOPPanicState(StatesGroup):
    to_data = State()


class I2CState(StatesGroup):
    to_category = State()
    to_chipset = State()
    to_data = State()


class AlphabetsState(StatesGroup):
    to_data = State()


class SwapState(StatesGroup):
    to_data = State()
    end = State()


class ITunesState(StatesGroup):
    to_data = State()


# USER
class EditPhoneNumberState(StatesGroup):
    new_phone_number = State()


class EditLanguageState(StatesGroup):
    language_code = State()


# TOOLS
class ImeiCheckerState(StatesGroup):
    imei = State()


class ImeiGeneratorState(StatesGroup):
    prefix = State()
    count = State()
