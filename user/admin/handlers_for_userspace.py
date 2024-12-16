import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile


from buttons.for_admin import user_space_management_menu
from buttons.for_others import skip_menu
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from queries.for_userspace import get_userspace_by_code_query, insert_userspace_query, delete_userspace_query, \
    get_all_user_spaces_query, get_userspace_by_id_query, update_userspace_query
from states.admin_state import AddUserSpaceState, DeleteUserSpaceState, EditUserSpaceState
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
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
                if user_space_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                user_space_data = get_userspace_by_code_query(user_space_code)
                if user_space_data is not None:
                    await send_protected_message(message, f"Bu Codeli User Space Mavjud!")
                    await state.clear()
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
                if user_space_name_uz in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

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
                if user_space_name_ru in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

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

            user_space_name = message.text
            if user_space_name in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                return

            await state.update_data(user_space_name_en=user_space_name)
            await send_protected_message(message, "Send photo:", reply_markup=skip_menu)
            await state.set_state(AddUserSpaceState.user_space_photo)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(AddUserSpaceState.user_space_photo)
async def add_user_space_photo(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                photo = None
                if message.text == 'Skip':
                    pass

                elif message.photo:
                    photo = message.photo[-1].file_id

                else:
                    await send_protected_message(message, "Invalid!")
                    return

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
                                       user_id=user_id,
                                       photo=photo)

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
                if user_space_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

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
                                f"Image: {user_space['photo']}\n"
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
async def edit_userspace(message: Message, state: FSMContext):
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

            if os.path.exists(user_spaces_file_path):
                os.remove(user_spaces_file_path)

            await send_protected_message(message, "Enter userspace ID:")
            await state.set_state(EditUserSpaceState.user_space_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_id)
async def edit_userspace_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                user_space_id = message.text
                if user_space_id in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await userspace_menu(message)
                    return

                if not user_space_id.isnumeric():
                    await send_protected_message(message, "ID must be numeric!")
                    await state.clear()
                    await userspace_menu(message)
                    return

                user_space_data = get_userspace_by_id_query(user_space_id)
                if user_space_data is None:
                    await send_protected_message(message, f"ID {user_space_id} User Space Mavjud Emas!")
                    return

                await send_protected_message(message, f"Enter new name uz:", reply_markup=skip_menu)
                await state.update_data(user_space_id=user_space_id)
                await state.set_state(EditUserSpaceState.user_space_new_name_uz)

            except Exception as e:
                print(str(e))
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_new_name_uz)
async def edit_userspace_new_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                new_name_uz = message.text
                if new_name_uz == "Skip":
                    new_name_uz = None

                else:
                    if new_name_uz in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await userspace_menu(message)
                        return

                await send_protected_message(message, f"Enter new name ru:", reply_markup=skip_menu)
                await state.update_data(user_space_new_name_uz=new_name_uz)
                await state.set_state(EditUserSpaceState.user_space_new_name_ru)

            except Exception as e:
                print(str(e))
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_new_name_ru)
async def edit_userspace_new_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                new_name_ru = message.text
                if new_name_ru == "Skip":
                    new_name_ru = None

                else:
                    if new_name_ru in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await userspace_menu(message)
                        return

                await send_protected_message(message, f"Enter new name en:", reply_markup=skip_menu)
                await state.update_data(user_space_new_name_ru=new_name_ru)
                await state.set_state(EditUserSpaceState.user_space_new_name_en)

            except Exception as e:
                print(str(e))
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_new_name_en)
async def edit_userspace_new_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                new_name_en = message.text
                if new_name_en == "Skip":
                    new_name_en = None

                else:
                    if new_name_en in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await userspace_menu(message)
                        return

                await send_protected_message(message, "Enter new code:", reply_markup=skip_menu)
                await state.update_data(user_space_new_name_en=new_name_en)
                await state.set_state(EditUserSpaceState.user_space_new_code)

            except Exception as e:
                print(str(e))
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_new_code)
async def edit_userspace_new_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            new_code = message.text
            if new_code == "Skip":
                new_code = None

            else:
                if new_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await userspace_menu(message)
                    return

                user_space_data = get_userspace_by_code_query(new_code)
                if user_space_data:
                    await send_protected_message(message, f"Bunday Kodli UserSpace Mavjud!")
                    await state.clear()
                    await userspace_menu(message)
                    return

            await state.update_data(user_space_new_code=new_code)
            await send_protected_message(message, "Send new photo:", reply_markup=skip_menu)
            await state.set_state(EditUserSpaceState.user_space_new_photo)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_userspace.message(EditUserSpaceState.user_space_new_photo)
async def edit_user_space_new_photo(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                photo = None
                if message.text == 'Skip':
                    pass

                elif message.photo:
                    photo = message.photo[-1].file_id

                else:
                    await send_protected_message(message, "Invalid!")
                    return

                state_data = await state.get_data()
                user_space_id = state_data.get("user_space_id")
                user_space_new_name_uz = state_data.get("user_space_new_name_uz")
                user_space_new_name_ru = state_data.get("user_space_new_name_ru")
                user_space_new_name_en = state_data.get("user_space_new_name_en")
                new_code = state_data.get("user_space_new_code")

                user_space_data = get_userspace_by_id_query(user_space_id)
                if user_space_new_name_uz is None:
                    user_space_new_name_uz = user_space_data.get("name_uz")

                if user_space_new_name_ru is None:
                    user_space_new_name_ru = user_space_data.get("name_ru")

                if user_space_new_name_en is None:
                    user_space_new_name_en = user_space_data.get("name_en")

                if new_code is None:
                    new_code = user_space_data.get("code")

                if photo is None:
                    photo = user_space_data.get("photo")

                update_userspace_query(userspace_id=user_space_id,
                                       new_name_uz=user_space_new_name_uz,
                                       new_name_ru=user_space_new_name_ru,
                                       new_name_en=user_space_new_name_en,
                                       code=new_code,
                                       new_photo=photo)

                await send_protected_message(message, "User Space edited successfully!")
                await send_protected_message(message, f"Name Uz: {user_space_new_name_uz}\n"
                                                      f"Name Ru: {user_space_new_name_ru}\n"
                                                      f"Name En: {user_space_new_name_en}\n"
                                                      f"Code: {new_code}\n", photo=photo)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await userspace_menu(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
