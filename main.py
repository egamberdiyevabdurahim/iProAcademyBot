from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from auth.auth_hendler import send_main_menu
from buttons.for_auth import choose_language_en, choose_language_uz, choose_language_ru
from buttons.for_user import user_main_menu_en, user_main_menu_uz, user_main_menu_ru
from database_config.config import TOKEN
from queries.for_users import get_user_by_telegram_id_query
from states.auth_state import RegisterState
from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered, get_user_data
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_active_message, not_registered_message

main_router = Router()
bot = Bot(token=TOKEN)


async def start_command_uz(message: Message, state: FSMContext):
    await send_protected_message(message, "Kerakli tilni tanglang", reply_markup=choose_language_uz)
    await state.set_state(RegisterState.language_code)


async def start_command_en(message: Message, state: FSMContext):
    await send_protected_message(message, content="Choose your language", reply_markup=choose_language_en)
    await state.set_state(RegisterState.language_code)


async def start_command_ru(message: Message, state: FSMContext):
    await send_protected_message(message, "Выберите свой язык", reply_markup=choose_language_ru)
    await state.set_state(RegisterState.language_code)


async def start_command_2_en(message: Message, user_data):
    await send_protected_message(message, f"Welcome to iPro Academy {user_data['first_name']}!")
    await send_protected_message(message, "Main Menu:", reply_markup=user_main_menu_en)


async def start_command_2_uz(message: Message, user_data):
    await send_protected_message(message, f"Assalomu Aleykum {user_data['first_name']}\niPro Acdemy-ga Xush Kelibsiz!")
    await send_protected_message(message, "Asosiy Menyu:", reply_markup=user_main_menu_uz)


async def start_command_2_ru(message: Message, user_data):
    await send_protected_message(message, f"Добро Пожаловать в iProAcademy {user_data['first_name']}!")
    await send_protected_message(message, "Главный Меню:", reply_markup=user_main_menu_ru)


@main_router.message(F.text=="Ishni Boshlash")
async def start_command_1(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await send_protected_message(message, "Menyuni tanlang 👇", reply_markup=user_main_menu_uz)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@main_router.message(F.text=="Поехали")
async def start_command_2(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await send_protected_message(message, "Выберите меню 👇", reply_markup=user_main_menu_ru)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@main_router.message(F.text=="Let's go")
async def start_command_3(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await send_protected_message(message, "Select menu 👇", reply_markup=user_main_menu_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@main_router.message(F.text.in_({"🔝Main Menu", "🔝Asosiy Menyu", "🔝Главное Меню"}))
async def back_to_main_menu(message: Message, state: FSMContext=None):
    await state.clear()
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            if message.text == "🔝Main Menu":
                await start_command_3(message)

            elif message.text == "🔝Asosiy Menyu":
                await start_command_1(message)

            elif message.text == "🔝Главное Меню":
                await start_command_2(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@main_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    is_registered = is_user_registered(message.from_user.id)
    if is_registered:
        user_data = get_user_data(message.from_user.id)
        if await is_active(message):
            await activity_maker(message)
            if user_data['language_code'] == 'ru':
                await start_command_2_ru(message, user_data)

            elif user_data['language_code'] == 'uz':
                await start_command_2_uz(message, user_data)

            else:
                await start_command_2_en(message, user_data)

        else:
            await send_main_menu(message, language_code=user_data['language_code'])

    else:
        if message.from_user.language_code == "uz":
            await start_command_uz(message, state)

        elif message.from_user.language_code == "ru":
            await start_command_ru(message, state)

        else:
            await start_command_en(message, state)