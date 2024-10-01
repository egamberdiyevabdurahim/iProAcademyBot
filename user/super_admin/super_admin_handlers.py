import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_super_admin import admin_management_menu, before_user_management_menu_super
from queries.for_users import get_user_by_telegram_id_query, get_all_admins_query, get_user_by_id_query, \
    add_admin_by_id_query, delete_user_query
from states.super_state import AddAdminState, DeleteAdminState
from user.admin.handlers_for_user_pending_user import user_management_show_users2
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, \
    not_super_admin_message

super_router = Router()


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



@super_router.message(F.text=="Show Admins")
async def show_all_admins(message: Message):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            user_file_path = os.path.join(BASE_PATH, "admins.txt")
            users = get_all_admins_query()
            with open(user_file_path, "w") as f:
                for user in users:
                    last_name = user['last_name'] or ""
                    f.write(f"ID: {user['id']}\n"
                            f"Telegram ID: {user['telegram_id']}\n"
                            f"First Name: {user['first_name']}\n"
                            f"Last Name: {last_name}\n"
                            f"Phone Number: {user['phone_number']}\n"
                            f"Language Code: {user['language_code']}\n"
                            f"IS ADMIN: {user['is_admin']}\n"
                            f"Created At: {user['created_at']}\n"
                            f"Updated At: {user['updated_at']}\n"
                            f"{'-' * 20}\n")

            if os.path.exists(user_file_path):
                cat = FSInputFile(user_file_path)
                await send_protected_message(message, document=cat)
            else:
                await send_protected_message(message, "The file does not exist.")
            # Clean up the file after sending
            if os.path.exists(user_file_path):
                os.remove(user_file_path)

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text=="Add Admin")
async def admin_management_add(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            await user_management_show_users2(message)
            await send_protected_message(message, "Userni ID-sini kiriting...")
            await state.set_state(AddAdminState.id_of)

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@super_router.message(AddAdminState.id_of)
async def admin_management_add_admin(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            user_id = message.text.strip()
            if user_id.isdigit():
                user_data = get_user_by_id_query(user_id)
                if user_data:
                    await send_protected_message(message, f"{user_data['first_name']} {user_data['last_name']} shu user admin bo'di!")
                    add_admin_by_id_query(user_id)
                    await state.clear()

                else:
                    await send_protected_message(message, "Bunday ID-lik user mavjud emas!")
                    return

            else:
                await send_protected_message(message, "ID-ning formatida kiriting!")
                return

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@super_router.message(F.text=="Delete Admin")
async def admin_management_delete(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            await show_all_admins(message)
            await send_protected_message(message, "Admin ID-sini kiriting...")
            await state.set_state(DeleteAdminState.id_of)

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@super_router.message(DeleteAdminState.id_of)
async def admin_management_delete_admin(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if get_user_by_telegram_id_query(message.from_user.id)['is_super'] is True:
            await activity_maker(message)

            user_id = message.text.strip()
            if user_id.isdigit():
                user_data = get_user_by_id_query(user_id)
                if user_data:
                    await send_protected_message(message, f"{user_data['first_name']} {user_data['last_name']} "
                                                          f"shu adminni o'chirildi!")
                    delete_user_query(int(user_id))
                    await state.clear()

                else:
                    await send_protected_message(message, "Bunday ID-lik user mavjud emas!")

            else:
                await send_protected_message(message, "ID-ning formatida kiriting!")

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)
