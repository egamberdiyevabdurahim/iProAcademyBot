from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from queries.for_alphabets import get_all_alphabets_query, get_alphabets_by_first_letter_query
from queries.for_aop_panic import get_all_aop_panics_query
from queries.for_chipset import get_all_chipsets_query
from queries.for_i2c import get_all_i2cs_by_category_id_query, get_i2c_by_category_and_chipset_query
from queries.for_i2c_category import get_all_i2c_categories_query, get_i2c_category_by_name_query
from queries.for_panic import get_all_panics_by_array_id_query
from queries.for_panic_array import get_all_panic_arrays_query, get_panic_array_by_name_query
from queries.for_userspace import get_all_user_spaces_query
from utils.addititons import ALPHABETS


main_menu_first_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ishni Boshlash")]],
    resize_keyboard=True)


main_menu_first_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поехали")]],
    resize_keyboard=True)


main_menu_first_en = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Let's go")]],
    resize_keyboard=True)


user_main_menu_en = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Apple"), KeyboardButton(text="Android")],
    [KeyboardButton(text="⚙️Setting"), KeyboardButton(text="ADMIN")],
    [KeyboardButton(text="🔝Back to Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


user_main_menu_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Apple"), KeyboardButton(text="Android")],
    [KeyboardButton(text="⚙️Настройки"), KeyboardButton(text="ADMIN")],
    [KeyboardButton(text="🔝Back to Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


user_main_menu_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Apple"), KeyboardButton(text="Android")],
    [KeyboardButton(text="⚙️Sozlamalar"), KeyboardButton(text="ADMIN")],
    [KeyboardButton(text="🔝Back to Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


profiles_menu_en = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Edit Phone Number"), KeyboardButton(text="Change Language")],
    [KeyboardButton(text="Show My Data"), KeyboardButton(text="💵Balance")],
    [KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


profiles_menu_ru = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Изменить Номер Телефона"), KeyboardButton(text="Изменить Язык")],
    [KeyboardButton(text="Показать Мои Данные"), KeyboardButton(text="💵Баланс")],
    [KeyboardButton(text="🔝Главное Меню")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите")


profiles_menu_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Telefon Raqamini O'zgartirish"), KeyboardButton(text="Tilni O'zgartirish")],
    [KeyboardButton(text="Ma'lumotlarimni ko'rish"), KeyboardButton(text="💵Balans")],
    [KeyboardButton(text="🔝Asosiy Menyu")]],
    resize_keyboard=True,
    input_field_placeholder="Tanlang")


async def apple_menu():
    # First keyboard
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="SMC PANIC - ASSERTION"))
    keyboard1.row(KeyboardButton(text="Userspace watchdog timeout"))
    keyboard1.row(KeyboardButton(text="i2c"), KeyboardButton(text="AOP PANIC"))

    # Second keyboard (Alphabet buttons)
    keyboard2 = ReplyKeyboardBuilder()
    for alphabet in ALPHABETS:
        alphabet_datas = get_alphabets_by_first_letter_query(alphabet)
        if len(alphabet_datas) > 0:
            keyboard2.button(text=alphabet)

    # Adjust the layout for keyboard2 to have 3 buttons per row
    keyboard2.adjust(3)
    keyboard2.row(KeyboardButton(text="🔝Main Menu"))

    # Manually combine the buttons from keyboard2 into keyboard1
    for row in keyboard2.export():
        keyboard1.row(*row)

    # Adjust layout for a maximum of 3 buttons per row and make the keyboard resizable
    data = keyboard1.as_markup(resize_keyboard=True)

    return data


async def panic_array_menu():
    keyboard = ReplyKeyboardBuilder()

    array_datas = get_all_panic_arrays_query()
    if len(array_datas) == 0:
        return None

    for array_data in array_datas:
        keyboard.row(KeyboardButton(text=array_data["name"]))

    keyboard.row(KeyboardButton(text="🔙Back To Apple Menu"), KeyboardButton(text="🔝Main Menu"))
    data = keyboard.as_markup()
    data.resize_keyboard = True
    return data


async def panic_menu(panic_array_name: str):
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="🔙Back To Array"), KeyboardButton(text="🔝Main Menu"))

    keyboard2 = ReplyKeyboardBuilder()

    array_data = get_panic_array_by_name_query(panic_array_name)

    arrays_datas = get_all_panics_by_array_id_query(array_data['id'])
    for array_data in arrays_datas:
        keyboard2.row(KeyboardButton(text=array_data["code"]))

    keyboard2.adjust(3)
    keyboard2.row(*keyboard1.buttons)

    data = keyboard2.as_markup()
    data.resize_keyboard = True
    return data


async def userspace_menu():
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="🔙Back To Apple Menu"), KeyboardButton(text="🔝Main Menu"))

    keyboard2 = ReplyKeyboardBuilder()

    userspace_datas = get_all_user_spaces_query()
    for userspace_data in userspace_datas:
        keyboard2.row(KeyboardButton(text=userspace_data["code"]))

    keyboard2.adjust(2)
    keyboard2.row(*keyboard1.buttons)

    data = keyboard2.as_markup()
    data.resize_keyboard = True
    return data


async def i2c_category_menu():
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="🔙Back To Apple Menu"), KeyboardButton(text="🔝Main Menu"))

    keyboard2 = ReplyKeyboardBuilder()

    categories_datas = get_all_i2c_categories_query()
    for category_data in categories_datas:
        keyboard2.row(KeyboardButton(text=category_data["name"]))

    keyboard2.adjust(2)
    keyboard2.row(*keyboard1.buttons)

    data = keyboard2.as_markup()
    data.resize_keyboard = True
    return data


async def i2c_menu(category_name: str):
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="🔙Back To i2c Menu"), KeyboardButton(text="🔝Main Menu"))

    keyboard2 = ReplyKeyboardBuilder()

    category_data = get_i2c_category_by_name_query(category_name)

    chipset_datas = get_all_chipsets_query()

    allowed_chipsets = list()
    for chipset in chipset_datas:
        i2c_data = get_i2c_by_category_and_chipset_query(chipset_id=chipset['id'], category_id=category_data['id'])
        if i2c_data is not None:
            allowed_chipsets.append(chipset['name'])

    if allowed_chipsets is None:
        return None

    for chipset_name in allowed_chipsets:
        keyboard2.button(text=f"{chipset_name}")

    keyboard2.adjust(2)
    keyboard2.row(*keyboard1.buttons)

    data = keyboard2.as_markup()
    data.resize_keyboard = True
    return data


async def aop_panic_menu():
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(KeyboardButton(text="🔙Back To Apple Menu"), KeyboardButton(text="🔝Main Menu"))

    keyboard2 = ReplyKeyboardBuilder()

    aop_panic_datas = get_all_aop_panics_query()
    for aop_panic_data in aop_panic_datas:
        keyboard2.row(KeyboardButton(text=aop_panic_data["code"]))

    keyboard2.adjust(2)
    keyboard2.row(*keyboard1.buttons)

    data = keyboard2.as_markup()
    data.resize_keyboard = True
    return data


async def alphabets_menu(alphabet_letter: str):
    # First keyboard for navigation
    keyboard1 = ReplyKeyboardBuilder()
    keyboard1.row(
        KeyboardButton(text="🔙Back To Apple Menu"),
        KeyboardButton(text="🔝Main Menu")
    )

    # Second keyboard for the alphabet data
    keyboard2 = ReplyKeyboardBuilder()

    # Fetch data based on the first letter
    alphabet_datas = get_alphabets_by_first_letter_query(alphabet_letter.upper())

    # If no data is found, return False (or None)
    if len(alphabet_datas) == 0:
        return None

    # Add buttons for each alphabet data
    for alphabet_data in alphabet_datas:
        keyboard2.row(KeyboardButton(text=alphabet_data["code"]))

    # Adjust the layout of the alphabet data buttons
    keyboard2.adjust(2)

    # Add the navigation buttons at the bottom
    keyboard2.row(*keyboard1.buttons)

    # Convert to markup and enable keyboard resizing
    data = keyboard2.as_markup(resize_keyboard=True)

    return data
