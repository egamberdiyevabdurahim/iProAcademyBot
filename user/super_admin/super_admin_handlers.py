from aiogram import Router, F
from aiogram.types import Message

from buttons.for_super_admin import admin_management_menu, user_management_menu_super, before_user_management_menu_super

from queries.for_users import get_user_by_telegram_id_query

from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import (not_registered_message, not_super_admin_message, is_active, not_active_message,
                             not_admin_message)

super_router = Router()


async def super_admin_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await send_protected_message(message, "Users Management Menu",
                                         reply_markup=before_user_management_menu_super)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text == "Users Management")
async def before_user_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
                await send_protected_message(message, "Admin Management",
                                             reply_markup=before_user_management_menu_super)
            else:
                await not_super_admin_message(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text == "User Management")
async def user_management_go(message: Message, user_id: int=None):
    if not user_id:
        user_id = message.from_user.id
    if is_user_registered(user_id):
        if await is_active(message, user_id):
            await activity_maker(message, user_id)

            user_data = get_user_by_telegram_id_query(user_id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            if user_data['is_super'] is True:
                await send_protected_message(message, "Admin Management", reply_markup=user_management_menu_super, user_id=user_id)
            else:
                await not_super_admin_message(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text=="Admin Management")
async def admin_management(message: Message):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            await send_protected_message(message, "Admin Management", reply_markup=admin_management_menu)

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text == "🔙Back to User Menu")
async def back_to_main_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await super_admin_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
