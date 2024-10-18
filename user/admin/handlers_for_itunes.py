import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import itunes_management_menu
from buttons.for_others import skip_menu
from queries.for_itunes import get_itunes_by_error_code_query, insert_itunes_query, update_itunes_query, \
    delete_itunes_query, get_all_itunes_query, get_itunes_by_id_query
from queries.for_model import get_all_models_query
from queries.for_users import get_user_by_telegram_id_query
from states.admin_state import AddITunesState, DeleteITunesState, EditITunesState
from utils.activity_maker import activity_maker
from utils.addititons import BUTTONS_AND_COMMANDS, BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_admin_message, not_active_message, not_registered_message

router_for_itunes = Router()


@router_for_itunes.message(F.text=="iTunes Management")
async def itunes_management_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "iTunes Management", reply_markup=itunes_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(F.text == "Add iTunes")
async def itunes_management_add_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Error Code:")
            await state.set_state(AddITunesState.itunes_error_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(AddITunesState.itunes_error_code)
async def itunes_management_add_error_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            error_code = message.text

            if error_code is None:
                await send_protected_message(message, "Error code cannot be empty.")
                await state.clear()
                return

            if error_code in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            if get_itunes_by_error_code_query(error_code) is not None:
                await send_protected_message(message, "Error code already exists.")
                await state.clear()
                return

            await send_protected_message(message, "Enter Uzbek Name:")
            await state.update_data(itunes_error_code=error_code)
            await state.set_state(AddITunesState.itunes_name_uz)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(AddITunesState.itunes_name_uz)
async def itunes_management_add_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            name_uz = message.text

            if name_uz is None:
                await send_protected_message(message, "Uzbek name cannot be empty.")
                await state.clear()
                return

            if name_uz in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            await send_protected_message(message, "Enter Russian Name:")
            await state.update_data(itunes_name_uz=name_uz)
            await state.set_state(AddITunesState.itunes_name_ru)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(AddITunesState.itunes_name_ru)
async def itunes_management_add_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            name_ru = message.text

            if name_ru is None:
                await send_protected_message(message, "Russian name cannot be empty.")
                await state.clear()
                return

            if name_ru in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            await send_protected_message(message, "Enter English Name:")
            await state.update_data(itunes_name_ru=name_ru)
            await state.set_state(AddITunesState.itunes_name_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(AddITunesState.itunes_name_en)
async def itunes_management_add_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            name_en = message.text

            if name_en is None:
                await send_protected_message(message, "English name cannot be empty.")
                await state.clear()
                return

            if name_en in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            itunes_data = await state.get_data()
            itunes_error_code = itunes_data.get('itunes_error_code')
            itunes_name_uz = itunes_data.get('itunes_name_uz')
            itunes_name_ru = itunes_data.get('itunes_name_ru')
            itunes_name_en = name_en
            user_id = get_user_by_telegram_id_query(message.from_user.id)['id']

            insert_itunes_query(error_code=itunes_error_code,
                                name_uz=itunes_name_uz,
                                name_ru=itunes_name_ru,
                                name_en=itunes_name_en,
                                user_id=user_id)

            await send_protected_message(message, "iTunes added successfully.")
            await state.clear()
            await itunes_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(F.text == "Delete iTunes")
async def itunes_management_delete_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Error Code:")
            await state.set_state(DeleteITunesState.itunes_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(DeleteITunesState.itunes_id)
async def itunes_management_delete_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            error_code = message.text

            if error_code is None:
                await send_protected_message(message, "Error code cannot be empty.")
                await state.clear()
                return

            if error_code in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            itunes_data = get_itunes_by_error_code_query(error_code)

            if itunes_data is None:
                await send_protected_message(message, f"iTunes with {error_code} is not available!")
                await state.clear()
                return

            delete_itunes_query(itunes_id=itunes_data['id'])

            await send_protected_message(message, "iTunes deleted successfully.")
            await state.clear()
            await itunes_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(F.text == "Show All iTunes")
async def itunes_management_show_all_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            itunes_file_path = os.path.join(BASE_PATH, "itunes.txt")

            itunes_datas = get_all_itunes_query()
            if len(itunes_datas) == 0:
                await send_protected_message(message, "No iTunes Found!")
                await itunes_management_go(message)
                return

            try:
                with open(itunes_file_path, "w") as f:
                    for itunes in itunes_datas:
                        f.write(f"ID: {itunes['id']}\n"
                                f"Name UZ: {itunes['name_uz']}\n"
                                f"Name RU: {itunes['name_ru']}\n"
                                f"Name EN: {itunes['name_en']}\n"
                                f"Error Code: {itunes['error_code']}\n"
                                f"Created At: {itunes['created_at']}\n"
                                f"Updated At: {itunes['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(itunes_file_path):
                    cat = FSInputFile(itunes_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(itunes_file_path):
                    os.remove(itunes_file_path)

                await itunes_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(F.text == "Edit iTunes")
async def itunes_management_edit_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Error Code:")
            await state.set_state(EditITunesState.itunes_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(EditITunesState.itunes_id)
async def itunes_management_edit_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            error_code = message.text

            if error_code is None:
                await send_protected_message(message, "Error code cannot be empty.")
                await state.clear()
                return

            if error_code in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            itunes_data = get_itunes_by_error_code_query(error_code)

            if itunes_data is None:
                await send_protected_message(message, f"iTunes with {error_code} is not available!")
                await state.clear()
                return

            await state.update_data(itunes_id=itunes_data['id'])
            await send_protected_message(message, "Enter New Name EN:", reply_markup=skip_menu)
            await state.set_state(EditITunesState.itunes_new_name_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(EditITunesState.itunes_new_name_en)
async def itunes_management_edit_new_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            new_name_en = message.text
            if new_name_en == "Skip":
                new_name_en = None

            else:
                if new_name_en is None:
                    await send_protected_message(message, "Name cannot be empty.")
                    await state.clear()
                    return

                if new_name_en in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

            await state.update_data(itunes_new_name_en=new_name_en)
            await send_protected_message(message, f"Enter New Name RU", reply_markup=skip_menu)
            await state.set_state(EditITunesState.itunes_new_name_ru)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(EditITunesState.itunes_new_name_ru)
async def itunes_management_edit_new_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            new_name_ru = message.text
            if new_name_ru == "Skip":
                new_name_ru = None

            else:
                if new_name_ru is None:
                    await send_protected_message(message, "Name cannot be empty.")
                    await state.clear()
                    return

                if new_name_ru in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

            await state.update_data(itunes_new_name_ru=new_name_ru)
            await send_protected_message(message, f"Enter New Name UZ", reply_markup=skip_menu)
            await state.set_state(EditITunesState.itunes_new_name_uz)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(EditITunesState.itunes_new_name_uz)
async def itunes_management_edit_new_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            new_name_uz = message.text
            if new_name_uz == "Skip":
                new_name_uz = None

            else:
                if new_name_uz is None:
                    await send_protected_message(message, "Name cannot be empty.")
                    await state.clear()
                    return

                if new_name_uz in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

            await state.update_data(itunes_new_name_uz=new_name_uz)
            await send_protected_message(message, "Enter New Error Code:", reply_markup=skip_menu)
            await state.set_state(EditITunesState.itunes_new_error_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_itunes.message(EditITunesState.itunes_new_error_code)
async def itunes_management_edit_new_error_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            new_error_code = message.text
            if new_error_code == "Skip":
                new_error_code = None

            else:
                if new_error_code is None:
                    await send_protected_message(message, "Error code cannot be empty.")
                    await state.clear()
                    return

                if new_error_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                if get_itunes_by_error_code_query(new_error_code) is not None:
                    await send_protected_message(message, "Error code already exists.")
                    await state.clear()
                    return

            itunes_data = await state.get_data()
            itunes_id = itunes_data['itunes_id']
            new_name_en = itunes_data.get('itunes_new_name_en')
            new_name_ru = itunes_data.get('itunes_new_name_ru')
            new_name_uz = itunes_data.get('itunes_new_name_uz')

            org_itunes_data = get_itunes_by_id_query(itunes_id)
            if new_name_en is None:
                new_name_en = org_itunes_data['name_en']

            if new_name_ru is None:
                new_name_ru = org_itunes_data['name_ru']

            if new_name_uz is None:
                new_name_uz = org_itunes_data['name_uz']

            if new_error_code is None:
                new_error_code = org_itunes_data['error_code']

            update_itunes_query(itunes_id=itunes_id,
                                new_name_en=new_name_en,
                                new_name_ru=new_name_ru,
                                new_name_uz=new_name_uz,
                                new_error_code=new_error_code)

            await send_protected_message(message, f"iTunes with error code {new_error_code} updated successfully!")
            await state.clear()
            await itunes_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
