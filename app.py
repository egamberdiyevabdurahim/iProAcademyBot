import asyncio

import schedule
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from database_config.config import TOKEN

from auth.auth_hendler import router

from buttons.for_auth import share_number_eng, share_number_rus, share_number_uz, choose_language_uz
from buttons.for_user import main_menu_first_en, main_menu_first_uz, main_menu_first_ru, user_main_menu_en, \
    user_main_menu_ru, user_main_menu_uz
from queries.for_users import get_user_by_telegram_id_query

from states.auth_state import RegisterState

from queries.for_pending_users import get_pending_user_by_telegram_id_query
from queries.for_running import if_not_used

from user.admin.admin_handlers import adm_router
from user.admin.handlers_for_alphabets import router_for_alphabets
from user.admin.handlers_for_aop_panic import router_for_aop_panic
from user.admin.handlers_for_chipset import router_for_chipset
from user.admin.handlers_for_i2c import router_for_i2c
from user.admin.handlers_for_i2c_category import router_for_i2c_category
from user.admin.handlers_for_panic import router_for_panic
from user.admin.handlers_for_panic_array import router_for_panic_array
from user.admin.handlers_for_user_pending_user import router_for_user_pending_user
from user.admin.handlers_for_userspace import router_for_userspace
from user.super_admin.super_admin_handlers import super_router
from user.user.handers_for_settings import user_setting_router

from user.user.handlers_for_alphabets import user_alphabets_router
from user.user.handlers_for_aop_panic import user_aop_panic_router
from user.user.handlers_for_i2c import user_i2c_router
from user.user.handlers_for_panic import user_panic_router
from user.user.handlers_for_userspace import user_userspace_router
from user.user.user_handlers import user_router

from user.for_end import end_router

from utils.activity_maker import activity_maker
from utils.for_auth import get_user_data, is_user_registered
from utils.important import balance_calculater
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message_uz, not_registered_message_en, not_registered_message_ru, is_active, \
    not_active_message, not_registered_message

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def start_command_uz(message: Message, is_pending, state: FSMContext):
    await send_protected_message(message, f'Assalomu Aleykum {message.from_user.first_name}\niPro Academy Botga Xush Kelibsiz!')

    if is_pending is not None:
        await send_protected_message(message, "Kerakli tilni tanglang", reply_markup=choose_language_uz)
        await state.set_state(RegisterState.language_code)

    else:
        await not_registered_message_uz(message)


async def start_command_en(message: Message, is_pending, state: FSMContext):
    await send_protected_message(message, f'Assalomu Aleykum {message.from_user.first_name}\nWelcome to iPro Academy!')

    if is_pending is not None:
        await send_protected_message(message, content="Choose your language", reply_markup=choose_language_uz)
        await state.set_state(RegisterState.language_code)

    else:
        await not_registered_message_en(message)


async def start_command_ru(message: Message, is_pending, state: FSMContext):
    await send_protected_message(message, f'{message.from_user.first_name} Добро пожаловать в Академию iPro!')

    if is_pending is not None:
        await send_protected_message(message, "Выберите свой язык", reply_markup=choose_language_uz)
        await state.set_state(RegisterState.language_code)

    else:
        await not_registered_message_ru(message)


async def start_command_2_en(message: Message, user_data):
    await send_protected_message(message, f"Welcome to iPro Academy {user_data['first_name']}!")
    # if user_data['is_super']:
    #     await send_protected_message(message, "Welcome Super Admin😊")
        # await adm_router.start(message, state)

    # else:
    await send_protected_message(message, "Main Menu:", reply_markup=main_menu_first_en)


async def start_command_2_uz(message: Message, user_data):
    await send_protected_message(message, f"Assalomu Aleykum {user_data['first_name']}\niPro Acdemy-ga Xush Kelibsiz!")
    # if user_data['is_super']:
    #     await send_protected_message(message, "Xush Kelobsiz Super Admin😊")
        # await adm_router.start(message, state)

    # else:
    await send_protected_message(message, "Asosiy Menyu:", reply_markup=main_menu_first_uz)


async def start_command_2_ru(message: Message, user_data):
    await send_protected_message(message, f"Добро Пожаловать в iProAcademy {user_data['first_name']}!")
    # if user_data['is_super']:
    #     await send_protected_message(message, "Добро пожаловать в Супер Администратор😊")
        # await adm_router.start(message, state)

    # else:
    await send_protected_message(message, "Главный Меню:", reply_markup=main_menu_first_ru)


@dp.message(F.text=="Ishni Boshlash")
async def start_command_1(message: Message):
    await send_protected_message(message, "Menyuni tanlang 👇", reply_markup=user_main_menu_uz)


@dp.message(F.text=="Поехали")
async def start_command_2(message: Message):
    await send_protected_message(message, "Выберите меню 👇", reply_markup=user_main_menu_ru)


@dp.message(F.text=="Let's go")
async def start_command_3(message: Message):
    await send_protected_message(message, "Select menu 👇", reply_markup=user_main_menu_en)


@dp.message(F.text=="🔝Back to Menu")
async def back_to_menu(message: Message, state: FSMContext):
    language = get_user_by_telegram_id_query(message.from_user.id)
    if language['language_code'] == 'ru':
        await start_command_2_ru(message, user_data=language)

    elif language['language_code'] == 'uz':
        await start_command_2_uz(message, user_data=language)

    else:
        await start_command_2_en(message, user_data=language)


@dp.message(F.text.in_({"🔝Main Menu", "🔝Asosiy Menyu", "🔝Главное Меню"}))
async def back_to_main_menu(message: Message):
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


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    is_registered = is_user_registered(message.from_user.id)
    is_pending = get_pending_user_by_telegram_id_query(message.from_user.id)
    if is_registered:
        await activity_maker(message)
        user_data = get_user_data(message.from_user.id)
        if user_data['language_code'] == 'ru':
            await start_command_2_ru(message, user_data)

        elif user_data['language_code'] == 'uz':
            await start_command_2_uz(message, user_data)

        else:
            await start_command_2_en(message, user_data)

    elif message.from_user.language_code == "uz":
        await start_command_uz(message, is_pending, state)

    elif message.from_user.language_code == "ru":
        await start_command_ru(message, is_pending, state)

    else:
        await start_command_en(message, is_pending, state)


async def schedule_task():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    if_not_used()
    dp.include_routers(router,
                       # ADMIN
                       adm_router,
                       # USER
                       user_router,
                       # ADMIN HANDLERS
                       router_for_alphabets,
                       router_for_aop_panic,
                       router_for_chipset,
                       router_for_i2c,
                       router_for_i2c_category,
                       router_for_panic,
                       router_for_panic_array,
                       router_for_user_pending_user,
                       router_for_userspace,
                       # USER HANDLERS
                       user_panic_router,
                       user_userspace_router,
                       user_aop_panic_router,
                       user_i2c_router,
                       user_alphabets_router,
                       user_setting_router,
                       # SUPER ADMIN
                       super_router,
                       end_router
                       )
    await dp.start_polling(bot)


async def init():
    schedule.every().day.at("00:10").do(lambda: asyncio.create_task(balance_calculater()))  # schedule async task
    await asyncio.gather(main(), schedule_task())  # run polling and schedule concurrently

if __name__ == '__main__':
    try:
        asyncio.run(init())
    except KeyboardInterrupt:
        print("Exit")