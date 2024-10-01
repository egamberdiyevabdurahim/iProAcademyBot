import os
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery

from buttons.for_admin import activate_user_menu
from queries.for_activity import get_all_activities_query, get_activities_by_user_id_query
from queries.for_balance import insert_balance_query, \
    get_active_balance_by_user_id_query, get_all_active_balance_query, get_all_balance_query
from queries.for_pending_users import get_pending_user_by_telegram_id_query, insert_pending_user_query, \
    get_all_pending_users_query, delete_pending_user_by_id_query
from queries.for_users import get_user_by_telegram_id_query, delete_user_query, get_all_users_query, \
    get_user_by_id_query

from states.admin_state import AddUserState, DeleteUserState, DeletePendingUserState, AddPendingUserState, \
    ShowActivityState, ActivateUserState
from user.admin.admin_handlers import user_management_go, pending_user_management_go
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_user_pending_user = Router()


# USER MANAGEMENT
@router_for_user_pending_user.message(F.text == "Add User")
async def user_management_add(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(AddUserState.telegram_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(AddUserState.telegram_id)
async def user_management_add_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                telegram_id = message.text
                pending_user = get_pending_user_by_telegram_id_query(int(telegram_id))
                user_data = get_user_by_telegram_id_query(int(telegram_id))

                if pending_user is not None:
                    await send_protected_message(message, f"Bu Telegram ID-ga ega foydalanuvchi mavjud ammo hali botga /start bermagan!\n"
                                         f"Foydalanuvchi malumotlari:\n"
                                         f"Telegram ID: {pending_user['telegram_id']}\n")

                elif user_data is not None:
                    await send_protected_message(message, f"Bu Telegram ID-ga ega foydalanuvchi mavjud!\n"
                                         f"Foydalanuvchi malumotlari:\n"
                                         f"Ismi: {user_data['first_name']}\nNomeri: {user_data['phone_number']}\n"
                                         f"Familiyasi: {user_data['last_name']}\nTelegram_id: {user_data['telegram_id']}\n"
                                         f"iS Admin: {user_data['is_admin']}\n")

                else:
                    insert_pending_user_query(int(telegram_id))
                    await send_protected_message(message, "Foydalanuvchi Muvaffaqiyatli Ro'yxatdan O'tkazildi\n"
                                         "Botga /start bersa bo'ldi!")

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(F.text == "Delete User")
async def user_management_delete(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(DeleteUserState.telegram_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(DeleteUserState.telegram_id)
async def user_management_delete_validate(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                telegram_id = message.text
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


@router_for_user_pending_user.message(F.text == "Edit User")
async def user_management_edit(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Comming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
        # await message.answer("Foydalanuvchi Telegram ID-sini kiriting: ")
        # await state.set_state(EditUserState.telegram_id)


# @router_for_user_pending_user.message(EditUserState.validate)
# async def user_management_edit_validate(message: Message, state: FSMContext):
#     telegram_id = message.text
#     user_data = get_user_by_telegram_id_query(int(telegram_id))
#     if user_data is not None:
#         last_name = user_data['last_name'] if user_data['last_name'] else "Mavjud Emas"
#         await message.answer(f"Foydalanuvchi Malumotlari:\n"
#                              f"Ismi: {user_data['first_name']}\nNomeri: {user_data['phone_number']}\n"
#                              f"Familiyasi: {last_name}\nTili: {user_data['language_code']}")
#         await state.update_data(telegram_id=telegram_id)
#         await state.set_state(EditUserState.menu)
#
#     else:
#         await message.answer("Bu Telegram IDlik user mavjud emas!")
#
#     await state.set_state(UserManagementMenuState.first)
#
#
# @router_for_user_pending_user.message(EditUserState.menu)
# async def user_management_edit_menu(message: Message, state: FSMContext):
#     await message.answer("Qaysi Malumotlarni O'zgartirish Kerakligini Tanlang:",
#                          reply_markup=edit_user_menu())
#     await state.set_state(EditUserState.validate_menu)
#
#
# @router_for_user_pending_user.message(EditUserState.validate_menu)
# async def user_management_edit_menu_validate(message: Message, state: FSMContext):
#     if message.text == "First Name":
#         await state.set_state(EditUserState.first_name)
#
#     elif message.text == "Phone Number":
#         await state.set_state(EditUserState.phone_number)
#
#     elif message.text == "Last Name":
#         await state.set_state(EditUserState.last_name)
#
#     elif message.text == "🔙Back":
#         await state.clear()
#         await state.set_state(EditUserState.first)
#
#     elif message.text == "��Main Menu":
#         await state.set_state(GoAdminMenuState.first)
#         await state.clear()
#
#
# @router_for_user_pending_user.message(EditUserState.first_name)
# async def user_management_edit_first_name(message: Message, state: FSMContext):
#     first_name = message.text
#     if first_name is None:
#         await message.answer("Ismi bo'sh qolishi mumkin emas!")
#
#     else:
#         state_data = state.get_data().__dict__
#         user_data = get_user_by_telegram_id_query(state_data['telegram_id'])
#         update_user_query(telegram_id=state_data["telegram_id"], first_name=user_data['first_name'],
#                           last_name=user_data['last_name'], language_code=user_data['language_code'],
#                           phone_number=user_data['phone_number'], user_id=user_data['id'])
#         await message.answer(f"Foydalanuvchi {first_name} nomli ismga o'zgartirildi!")
#     await state.set_state(EditUserState.menu)
#
#
# @router_for_user_pending_user.message(EditUserState.phone_number)
# async def user_management_edit_phone_number(message: Message, state: FSMContext):
#     phone_number = message.text
#     if not re.match(PATTERN, phone_number):
#         await message.answer("Nomer formati xato!")
#
#     else:
#         state_data = state.get_data().__dict__
#         user_data = get_user_by_telegram_id_query(state_data['telegram_id'])
#         update_user_query(telegram_id=state_data["telegram_id"], first_name=user_data['first_name'],
#                           last_name=user_data['last_name'], language_code=user_data['language_code'],
#                           phone_number=phone_number, user_id=user_data['id'])
#         await message.answer(f"Foydalanuvchi {phone_number} nomerga o'zgartirildi!")
#     await state.set_state(EditUserState.menu)
#
#
# @router_for_user_pending_user.message(EditUserState.last_name)
# async def user_management_edit_last_name(message: Message, state: FSMContext):
#     last_name = message.text
#     if last_name is None:
#         await message.answer("Familiyasi bo'sh qolishi mumkin emas!")
#
#     else:
#         state_data = state.get_data().__dict__
#         user_data = get_user_by_telegram_id_query(state_data['telegram_id'])
#         update_user_query(telegram_id=state_data["telegram_id"], first_name=user_data['first_name'],
#                           last_name=last_name, language_code=user_data['language_code'],
#                           phone_number=user_data['phone_number'], user_id=user_data['id'])
#         await message.answer(f"Foydalanuvchi {last_name} nomli familiyaga o'zgartirildi!")
#     await state.set_state(EditUserState.menu)


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


@router_for_user_pending_user.message(F.text == "Show Users")
async def user_management_show_users(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
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


@router_for_user_pending_user.message(F.text == "Activate User")
async def user_management_activate_user(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await user_management_show_users2(message)
            await send_protected_message(message, "Foydalanuvchi ID-sini kiriting: ")
            await state.set_state(ActivateUserState.user_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(ActivateUserState.user_id)
async def user_management_activate_user_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            id_of = message.text
            if id_of is None:
                await send_protected_message(message, "Foydalanuvchi ID-si xato!")
                return

            user = get_user_by_id_query(id_of)
            if user is None:
                await send_protected_message(message, "Bunday foydalanuvchi mavjud emas!")
                return

            if get_active_balance_by_user_id_query(id_of):
                await send_protected_message(message, "Bu Foydalauvchi Allaqachon Aktiv!")
                return

            await state.update_data(user_id=id_of)

            await send_protected_message(message, "Boshlanish Vaqtini Kiriting yoki skip yozin skip uchun(YYYY.MM.DD):")
            await state.set_state(ActivateUserState.starts_at)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(ActivateUserState.starts_at)
async def user_management_activate_user_starts_at(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            try:
                user_data = get_user_by_telegram_id_query(message.from_user.id)
                if user_data['is_admin'] is False:
                    await not_admin_message(message)
                    return

                starts_at = message.text
                if starts_at is None:
                    await send_protected_message(message, "Boshlanish Vaqti bo'sh bo'ishi mumkin emas!")
                    return

                if starts_at.lower() == "skip":
                    await state.update_data(starts_at=datetime.now().date())

                else:
                    if datetime.strptime(starts_at, "%Y.%m.%d"):
                        starts_at_date = datetime.strptime(starts_at, "%Y.%m.%d")

                    else:
                        await send_protected_message(message, "Boshlanish Vaqti formati yaroqsiz!")
                        return

                    await state.update_data(starts_at=starts_at_date)

                await send_protected_message(message, "Choose Duration:", reply_markup=activate_user_menu)
                await state.set_state(ActivateUserState.duration)

            except ValueError:
                await send_protected_message(message, "Boshlanish vaqti formati yaroqsiz!")
                return

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.callback_query(ActivateUserState.duration)
async def user_management_activate_user_duration(callback: CallbackQuery, state: FSMContext):
    if is_user_registered(callback.from_user.id):
        if await is_active(callback.message, user_id=callback.from_user.id):
            await activity_maker(callback.message, user_id=callback.from_user.id)

            user_data = get_user_by_telegram_id_query(callback.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(callback.message)
                return

            state_data = await state.get_data()
            user_id = state_data.get('user_id')
            starts_at = state_data.get('starts_at')
            duration = callback.data

            for_month = False
            for_three_month = False
            for_six_month = False
            for_nine_month = False
            for_year = False

            end_date = None

            if duration == "for_month":
                for_month = True
                end_date = starts_at + timedelta(days=30)

            elif duration == "for_three_month":
                for_three_month = True
                end_date = starts_at + timedelta(days=90)

            elif duration == "for_six_month":
                for_six_month = True
                end_date = starts_at + timedelta(days=180)

            elif duration == "for_nine_month":
                for_nine_month = True
                end_date = starts_at + timedelta(days=270)

            elif duration == "for_year":
                for_year = True
                end_date = starts_at + timedelta(days=365)

            insert_balance_query(user_id=user_id, starts_at=starts_at, for_month=for_month,
                                 for_three_month=for_three_month, for_six_month=for_six_month,
                                 for_nine_month=for_nine_month, for_year=for_year, ends_at=end_date)

            await callback.message.delete_reply_markup()
            await send_protected_message(callback.message, f"Foydalanuvchi {user_id}. {duration}.")
            await state.clear()
            await user_management_go(callback.message, callback.from_user.id)


        else:
            await not_active_message(callback.message)

    else:
        await not_registered_message(callback.message)


@router_for_user_pending_user.message(F.text == "Show Active Users")
async def user_management_show_active_users(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "active_users.txt")

            try:
                active_balances = get_all_active_balance_query()
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


@router_for_user_pending_user.message(F.text == "Show All Balances")
async def user_management_show_active_users(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "balances.txt")

            try:
                active_balances = get_all_balance_query()
                with open(user_file_path, "w") as f:
                    for balance in active_balances:
                        user = get_user_by_id_query(user_id=balance['user_id'])
                        f.write(f"ID: {balance['id']}\n"
                                f"User: {user['first_name']}\n"
                                f"Started At: {balance['starts_at']}\n"
                                f"Ends At: {balance['ends_at']}\n"
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


# PENDING USER MANAGEMENT
@router_for_user_pending_user.message(F.text == "Add Pending User")
async def pending_user_management_add(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(AddPendingUserState.telegram_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(AddPendingUserState.telegram_id)
async def pending_user_management_add_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                telegram_id = message.text
                pending_user = get_pending_user_by_telegram_id_query(int(telegram_id))
                user_data = get_user_by_telegram_id_query(int(telegram_id))

                if pending_user is not None:
                    await send_protected_message(message, f"Bu Telegram ID-ga ega foydalanuvchi mavjud ammo hali botga /start bermagan!\n"
                                         f"Foydalanuvchi malumotlari:\n"
                                         f"Telegram ID: {pending_user['telegram_id']}\n")

                elif user_data is not None:
                    await send_protected_message(message, f"Bu Telegram ID-ga ega foydalanuvchi mavjud!\n"
                                         f"Foydalanuvchi malumotlari:\n"
                                         f"Ismi: {user_data['first_name']}\nNomeri: {user_data['phone_number']}\n"
                                         f"Familiyasi: {user_data['last_name']}\nTelegram_id: {user_data['telegram_id']}\n"
                                         f"Language Code: {user_data['language_code']}\n"
                                         f"iS Admin: {user_data['is_admin']}\n")

                else:
                    insert_pending_user_query(int(telegram_id))
                    await send_protected_message(message, "Foydalanuvchi Muvaffaqiyatli Ro'yxatdan O'tkazildi\n"
                                         "Botga /start bersa bo'ldi!")

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await pending_user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(F.text == "Delete Pending User")
async def pending_user_management_delete(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Foydalanuvchi Telegram ID-sini kiriting: ")
            await state.set_state(DeletePendingUserState.telegram_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(DeletePendingUserState.telegram_id)
async def pending_user_management_delete_validate(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                telegram_id = message.text
                user_data = get_pending_user_by_telegram_id_query(int(telegram_id))
                if user_data is not None:
                    await send_protected_message(message, f"Pending User Info:\n"
                                         f"ID: {user_data['id']}\n"
                                         f"Telegram ID: {user_data['telegram_id']}\n"
                                         f"Created At: {user_data['created_at']}")

                    await send_protected_message(message, "Pending User Deleted Successfully!")
                    delete_pending_user_by_id_query(user_data['id'])
                else:
                    await send_protected_message(message, "Bu Telegram IDlik pending user mavjud emas!")
            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await pending_user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(F.text == "Show Pending Users")
async def pending_user_management_show(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            user_file_path = os.path.join(BASE_PATH, "pending_users.txt")

            users = get_all_pending_users_query()
            if len(users) == 0:
                await send_protected_message(message, "There are no Pending Users!")
                await pending_user_management_go(message)
                return

            try:
                with open(user_file_path, "w") as f:
                    for user in users:
                        f.write(f"ID: {user['id']}\n"
                                f"Telegram ID: {user['telegram_id']}\n"
                                f"Created At: {user['created_at']}\n"
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

                await pending_user_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


# ACTIVITY
@router_for_user_pending_user.message(F.text == "Show All Users Log")
async def activity_management_show(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
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


@router_for_user_pending_user.message(F.text == "Show User Log")
async def activity_management_show(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await user_management_show_users2(message)
            await send_protected_message(message, "Enter user's ID:")
            await state.set_state(ShowActivityState.user_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_user_pending_user.message(ShowActivityState.user_id)
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
