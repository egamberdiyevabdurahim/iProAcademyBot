import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile


from buttons.for_admin import user_space_management_menu
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from queries.for_userspace import get_userspace_by_code_query, insert_userspace_query, delete_userspace_query, \
    get_all_user_spaces_query
from states.admin_state import AddUserSpaceState, DeleteUserSpaceState
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_userspace = Router()


@router_for_userspace.message(F.text == "UserSpace Management")
async def userspace_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "UserSpace Management", reply_markup=user_space_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(F.text == "Add User Space")
async def add_userspace(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter User Space's Code:")
            await state.set_state(AddUserSpaceState.user_space_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(AddUserSpaceState.user_space_code)
async def add_userspace_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                user_space_code = message.text
                user_space_data = get_userspace_by_code_query(user_space_code)
                if user_space_data is not None:
                    await send_protected_message(message, f"Bu Codeli User Space Mavjud!")
                    return

                await state.update_data(user_space_code=user_space_code)
                await send_protected_message(message, "Enter User Space's Uzbek Name:")
                await state.set_state(AddUserSpaceState.user_space_name_uz)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(AddUserSpaceState.user_space_name_uz)
async def add_userspace_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                user_space_name_uz = message.text
                await state.update_data(user_space_name_uz=user_space_name_uz)

                await send_protected_message(message, "Enter User Space's Russian Name:")
                await state.set_state(AddUserSpaceState.user_space_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(AddUserSpaceState.user_space_name_ru)
async def add_userspace_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                user_space_name_ru = message.text
                await state.update_data(user_space_name_ru=user_space_name_ru)

                await send_protected_message(message, "Enter User Space's English Name:")
                await state.set_state(AddUserSpaceState.user_space_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(AddUserSpaceState.user_space_name_en)
async def add_userspace_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                user_space_name = message.text
                await state.update_data(user_space_name_en=user_space_name)

                user_space_data = await state.get_data()
                user_space_code = user_space_data['user_space_code']
                user_space_name_uz = user_space_data['user_space_name_uz']
                user_space_name_ru = user_space_data['user_space_name_ru']
                user_space_name_en = user_space_data['user_space_name_en']
                user_id = get_user_by_telegram_id_query(message.from_user.id)['id']

                await send_protected_message(message, "UserSpace Created Successfully!")
                insert_userspace_query(name_uz=user_space_name_uz,
                                       name_ru=user_space_name_ru,
                                       name_en=user_space_name_en,
                                       code=user_space_code,
                                       user_id=user_id)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(F.text == "Delete User Space")
async def delete_userspace(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter User Space's Code:")
            await state.set_state(DeleteUserSpaceState.user_space_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(DeleteUserSpaceState.user_space_id)
async def delete_userspace_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                user_space_code = message.text
                user_space_data = get_userspace_by_code_query(user_space_code)
                if user_space_data is None:
                    await send_protected_message(message, f"Bu Codeli User Space Mavjud Emas!")
                    return

                await send_protected_message(message, f"ID: {user_space_data['id']}\n"
                                     f"Name UZ: {user_space_data['name_uz']}\n"
                                     f"Name RU: {user_space_data['name_ru']}\n"
                                     f"Name EN: {user_space_data['name_en']}\n"
                                     f"Code: {user_space_data['code']}\n"
                                     f"User ID: {get_user_by_id_query(user_space_data['user_id'])['first_name']}\n")
                await send_protected_message(message, "User Space Deleted Successfully!")
                delete_userspace_query(user_space_data['id'])

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(F.text == "Show User Spaces")
async def show_user_spaces(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            user_spaces_file_path = os.path.join(BASE_PATH, "all_userspace.txt")

            user_spaces = get_all_user_spaces_query()
            if len(user_spaces) == 0:
                await send_protected_message(message, "There are no User Spaces!")
                await userspace_menu(message)
                return

            try:
                with open(user_spaces_file_path, "w") as f:
                    for user_space in user_spaces:
                        f.write(f"ID: {user_space['id']}\n"
                                f"Name UZ: {user_space['name_uz']}\n"
                                f"Name RU: {user_space['name_ru']}\n"
                                f"Name EN: {user_space['name_en']}\n"
                                f"Code: {user_space['code']}\n"
                                f"User: {get_user_by_id_query(user_space['user_id'])['first_name']}\n"
                                f"Created At: {user_space['created_at']}\n"
                                f"Updated At: {user_space['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(user_spaces_file_path):
                    cat = FSInputFile(user_spaces_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(user_spaces_file_path):
                    os.remove(user_spaces_file_path)

                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(F.text == "Edit User Space")
async def edit_userspace(message: Message):
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
