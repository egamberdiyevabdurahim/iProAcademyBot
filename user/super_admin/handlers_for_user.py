import os
from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from buttons.for_super_admin import activate_user_menu
from database_config.config import TOKEN
from queries.for_activity import get_all_activities_query, get_activities_by_user_id_query
from queries.for_balance import get_all_active_balance_query, insert_balance_query, get_active_balance_by_user_id_query
from queries.for_users import get_user_by_telegram_id_query, get_all_admins_query, get_user_by_id_query, \
    add_admin_by_id_query, delete_user_query, get_inactive_users_query, get_all_users_query
from states.super_state import (AddAdminState, DeleteAdminState, ScheduleActivateUser, ActivateUserState,
                                DeleteUserState, ShowActivityState)
from user.super_admin.super_admin_handlers import user_management_go
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, not_super_admin_message, is_active, not_active_message, \
    not_admin_message

router_for_user_super = Router()
bot = Bot(token=TOKEN)


# USER MANAGEMENT
@router_for_user_super.message(F.text == "Delete User")
async def user_management_delete(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(DeleteUserState.telegram_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(DeleteUserState.telegram_id)
async def user_management_delete_validate(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            try:
                telegram_id = message.text
                if not telegram_id.isnumeric():
                    await send_protected_message(message, "Bu telegram ID xato!")
                    return
                user_data = get_user_by_telegram_id_query(int(telegram_id))
                if user_data is not None:
                    await send_protected_message(message, f"Foydalanuvchi Malumotlari:\n"
                                         f"Ismi: {user_data['first_name']}\nNomeri: {user_data['phone_number']}\n"
                                         f"Familiyasi: {user_data['last_name']}\nTili: {user_data['language_code']}")

                    await send_protected_message(message, "User Deleted Successfully!")
                    delete_user_query(user_data['id'])
                else:
                    await send_protected_message(message, "Bu Telegram IDlik user mavjud emas!")

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(F.text == "Edit User")
async def user_management_edit(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await send_protected_message(message, "Comming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


async def user_management_show_users2(message: Message):
    user_file_path = os.path.join(BASE_PATH, "users.txt")
    users = get_all_users_query()
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


@router_for_user_super.message(F.text == "Show Users")
async def user_management_show_users(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "users.txt")

            try:
                users = get_all_users_query()
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

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")

            finally:
                # Clean up the file after sending
                if os.path.exists(user_file_path):
                    os.remove(user_file_path)

                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


# ACTIVITY
@router_for_user_super.message(F.text == "Show All Users Log")
async def activity_management_show(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "activity.txt")

            activities = get_all_activities_query()
            if len(activities) == 0:
                await send_protected_message(message, "There are no activities!")
                await user_management_go(message)
                return

            try:
                with open(user_file_path, "w") as f:
                    for activity in activities:
                        f.write(f"ID: {activity['id']}\n"
                                f"USER ID: {activity['user_id']}\n"
                                f"TEXT: {activity['text']}\n"
                                f"Created At: {activity['created_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(user_file_path):
                    cat = FSInputFile(user_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(user_file_path):
                    os.remove(user_file_path)

                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(F.text == "Show User Log")
async def activity_management_show(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await user_management_show_users2(message)
            await send_protected_message(message, "Enter user's ID:")
            await state.set_state(ShowActivityState.user_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(ShowActivityState.user_id)
async def activity_management_show_validate(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            if message.text.isnumeric():
                user_data = get_user_by_id_query(message.text)
                if user_data is None:
                    await send_protected_message(message, "User not found!")
                    return

                user_dat = get_user_by_telegram_id_query(message.from_user.id)
                if user_dat['is_admin'] is False:
                    await not_admin_message(message)
                    return

                user_file_path = os.path.join(BASE_PATH, f"user_{user_data['id']}_activity.txt")

                try:
                    user_id = message.text
                    user_activities = get_activities_by_user_id_query(user_id)

                    if len(user_activities) == 0:
                        await send_protected_message(message, f"User with ID {user_id} has no logs!")
                        return

                    with open(user_file_path, "w") as f:
                        for activity in user_activities:
                            f.write(f"ID: {activity['id']}\n"
                                    f"TEXT: {activity['text']}\n"
                                    f"Created At: {activity['created_at']}\n"
                                    f"{'-' * 20}\n")

                    if os.path.exists(user_file_path):
                        cat = FSInputFile(user_file_path)
                        await send_protected_message(message, document=cat)
                    else:
                        await send_protected_message(message, "The file does not exist.")

                except Exception as e:
                    await send_protected_message(message, f"An error occurred: {e}")

                finally:
                    # Clean up the file after sending
                    if os.path.exists(user_file_path):
                        os.remove(user_file_path)

                    await user_management_go(message)
            else:
                await send_protected_message(message, "Please enter a valid user ID!")
                await state.clear()
                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(F.text=="Show Admins")
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


@router_for_user_super.message(F.text=="Add Admin")
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


@router_for_user_super.message(AddAdminState.id_of)
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
                    await state.clear()
                    return

            else:
                await send_protected_message(message, "ID-ning formatida kiriting!")
                await state.clear()
                return

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(F.text=="Delete Admin")
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


@router_for_user_super.message(DeleteAdminState.id_of)
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
                    await state.clear()

            else:
                await send_protected_message(message, "ID-ning formatida kiriting!")
                await state.clear()

        else:
            await not_super_admin_message(message)

    else:
        await not_registered_message(message)


async def user_management_show_inactive_users(message: Message):
    user_file_path = os.path.join(BASE_PATH, "inactive_users.txt")
    users = get_inactive_users_query()
    with open(user_file_path, "w") as f:
        for user in users:
            last_name = user['last_name'] or None
            f.write(f"ID: {user[0]}\n"
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


@router_for_user_super.message(F.text == "Activate User")
async def user_management_activate_user(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await user_management_show_inactive_users(message)
            await send_protected_message(message, "Foydalanuvchi ID-sini kiriting: ")
            await state.set_state(ActivateUserState.user_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(ActivateUserState.user_id)
async def user_management_activate_user_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            id_of = message.text
            if id_of is None:
                await send_protected_message(message, "Foydalanuvchi ID-si xato!")
                await state.clear()
                return

            if not id_of.isnumeric():
                await send_protected_message(message, "Foydalanuvchi ID-si xato!")
                await state.clear()
                return

            user = get_user_by_id_query(id_of)
            if user is None:
                await send_protected_message(message, "Bunday foydalanuvchi mavjud emas!")
                await state.clear()
                return

            if get_active_balance_by_user_id_query(id_of):
                await send_protected_message(message, "Bu Foydalauvchi Allaqachon Aktiv!")
                await state.clear()
                return

            await state.update_data(user_id=id_of)

            await send_protected_message(message, "Choose Duration:", reply_markup=activate_user_menu)
            await state.set_state(ActivateUserState.duration)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.callback_query(ActivateUserState.duration)
async def user_management_activate_user_duration(callback: CallbackQuery, state: FSMContext):
    if is_user_registered(callback.from_user.id):
        if await is_active(callback.message, user_id=callback.from_user.id):
            await activity_maker(callback.message, user_id=callback.from_user.id)

            state_data = await state.get_data()
            user_id = state_data.get('user_id')
            starts_at = datetime.date(datetime.now())
            duration = callback.data

            for_month = False
            for_three_month = False
            for_six_month = False
            for_nine_month = False
            for_year = False

            end_date = None
            eng_name = ''
            ru_name = ''
            uz_name = ''

            if duration == "for_month":
                for_month = True
                end_date = starts_at + timedelta(days=30)
                eng_name = "30 days"
                ru_name = "30 дней"
                uz_name = "30 kun"

            elif duration == "for_three_month":
                for_three_month = True
                end_date = starts_at + timedelta(days=90)
                eng_name = "90 days"
                ru_name = "90 дней"
                uz_name = "90 kun"

            elif duration == "for_six_month":
                for_six_month = True
                end_date = starts_at + timedelta(days=180)
                eng_name = "180 days"
                ru_name = "180 дней"
                uz_name = "180 kun"

            elif duration == "for_nine_month":
                for_nine_month = True
                end_date = starts_at + timedelta(days=270)
                eng_name = "270 days"
                ru_name = "270 дней"
                uz_name = "270 kun"

            elif duration == "for_year":
                for_year = True
                end_date = starts_at + timedelta(days=365)
                eng_name = "365 days"
                ru_name = "365 дней"
                uz_name = "365 kun"

            insert_balance_query(user_id=user_id, starts_at=starts_at, for_month=for_month,
                                 for_three_month=for_three_month, for_six_month=for_six_month,
                                 for_nine_month=for_nine_month, for_year=for_year, ends_at=end_date)

            user_data = get_user_by_id_query(user_id)

            await callback.message.delete_reply_markup()
            await send_protected_message(callback.message, f"{user_id} - id lik {user_data['first_name']}\n"
                                                           f"{uz_name}-ga aktivatsiya qilindi✅")
            text_uz = f"{user_data['first_name']} - Sizni Balansingiz {uz_name}-ga To'dirildi🎉"
            text_ru = f"{user_data['first_name']} - Ваш баланс был увеличен на {ru_name}🎉"
            text_en = f"{user_data['first_name']} - Your balance has been increased for {eng_name}🎉"

            text = None
            if user_data['language_code'] == "en":
                text = text_en

            elif user_data['language_code'] == "ru":
                text = text_ru

            elif user_data['language_code'] == "uz":
                text = text_uz

            await bot.send_message(chat_id=user_data['telegram_id'], text=text)
            await state.clear()
            await user_management_go(callback.message, callback.from_user.id)


        else:
            await not_active_message(callback.message)

    else:
        await not_registered_message(callback.message)


@router_for_user_super.message(F.text == "Show Active Users")
async def user_management_show_active_users(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "active_users.txt")

            try:
                active_balances = get_all_active_balance_query()
                if len(active_balances) == 0:
                    await send_protected_message(message, "No active users found!")
                    return
                with open(user_file_path, "w") as f:
                    for balance in active_balances:
                        days_left = balance['ends_at'] - datetime.date(datetime.now())
                        user = get_user_by_id_query(user_id=balance['user_id'])
                        f.write(f"ID: {balance['id']}\n"
                                f"User: {user['first_name']}\n"
                                f"Started At: {balance['starts_at']}\n"
                                f"Ends At: {balance['ends_at']}\n"
                                f"Days Left: {days_left}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(user_file_path):
                    cat = FSInputFile(user_file_path)
                    await send_protected_message(message, document=cat)

                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")

            finally:
                # Clean up the file after sending
                if os.path.exists(user_file_path):
                    os.remove(user_file_path)

                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(F.text == "Schedule Activate User")
async def user_management_schedule_activate_user(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await user_management_show_users2(message)
            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(ScheduleActivateUser.user_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.message(ScheduleActivateUser.user_id)
async def user_management_activate_user_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            id_of = message.text
            if id_of is None:
                await send_protected_message(message, "Foydalanuvchi Telegram ID-si xato!")
                await state.clear()
                return

            if not id_of.isnumeric():
                await send_protected_message(message, "Foydalanuvchi Telegram ID-si xato!")
                await state.clear()
                return

            user = get_user_by_telegram_id_query(id_of)
            if user is None:
                await send_protected_message(message, "Bunday foydalanuvchi mavjud emas!")
                await state.clear()
                return

            await state.update_data(user_id=user['id'])

            await send_protected_message(message, "Choose Duration:", reply_markup=activate_user_menu)
            await state.set_state(ScheduleActivateUser.duration)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_super.callback_query(ScheduleActivateUser.duration)
async def user_management_activate_user_duration(callback: CallbackQuery, state: FSMContext):
    if is_user_registered(callback.from_user.id):
        if await is_active(callback.message, user_id=callback.from_user.id):
            await activity_maker(callback.message, user_id=callback.from_user.id)

            state_data = await state.get_data()
            user_id = state_data.get('user_id')
            starts_at = datetime.date(datetime.now())
            duration = callback.data

            for_month = False
            for_three_month = False
            for_six_month = False
            for_nine_month = False
            for_year = False

            end_date = None
            uz_name = ''

            if duration == "for_month":
                for_month = True
                end_date = starts_at + timedelta(days=30)
                uz_name = "30 kun"

            elif duration == "for_three_month":
                for_three_month = True
                end_date = starts_at + timedelta(days=90)
                uz_name = "90 kun"

            elif duration == "for_six_month":
                for_six_month = True
                end_date = starts_at + timedelta(days=180)
                uz_name = "180 kun"

            elif duration == "for_nine_month":
                for_nine_month = True
                end_date = starts_at + timedelta(days=270)
                uz_name = "270 kun"

            elif duration == "for_year":
                for_year = True
                end_date = starts_at + timedelta(days=365)
                uz_name = "365 kun"

            active = True
            balance = get_active_balance_by_user_id_query(user_id)
            if balance is not None:
                starts_at = starts_at+timedelta(days=1)
                end_date_1 = (balance['ends_at'] - datetime.date(datetime.now())).days
                end_date = timedelta(days=end_date_1+1) + end_date
                active = False

            insert_balance_query(user_id=user_id, starts_at=starts_at, for_month=for_month,
                                 for_three_month=for_three_month, for_six_month=for_six_month,
                                 for_nine_month=for_nine_month, for_year=for_year, ends_at=end_date,
                                 is_active=active)

            user_data = get_user_by_id_query(user_id)

            await callback.message.delete_reply_markup()
            await send_protected_message(callback.message, f"{user_id} - id lik {user_data['first_name']}\n"
                                                           f"{uz_name}-ga aktivatsiya qilindi✅")
            await state.clear()
            await user_management_go(callback.message, callback.from_user.id)

        else:
            await not_active_message(callback.message)

    else:
        await not_registered_message(callback.message)