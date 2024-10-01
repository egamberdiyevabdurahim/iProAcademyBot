import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import chipset_management_menu
from queries.for_chipset import get_chipset_by_name_query, insert_chipset_query, delete_chipset_query, \
    get_all_chipsets_query, update_chipset_query
from queries.for_users import get_user_by_telegram_id_query
from states.admin_state import AddChipsetState, DeleteChipsetState, EditChipsetState
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_chipset = Router()


@router_for_chipset.message(F.text == "Chipset Management")
async def before_chipset_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Chipset Management", reply_markup=chipset_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(F.text == "Add Chipset")
async def add_chipset(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Chipset's Name:")
            await state.set_state(AddChipsetState.chipset_name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(AddChipsetState.chipset_name)
async def add_chipset_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                chipset_name = message.text
                chipset_data = get_chipset_by_name_query(chipset_name)
                if chipset_data is not None:
                    await send_protected_message(message, f"Bu Chipset Mavjud!")
                    return

                await send_protected_message(message, "Chipset Created Successfully!")
                insert_chipset_query(chipset_name)

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_chipset_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(F.text == "Delete Chipset")
async def delete_chipset(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Chipset's Name:")
            await state.set_state(DeleteChipsetState.chipset_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(DeleteChipsetState.chipset_id)
async def delete_chipset_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                chipset_name = message.text
                chipset_data = get_chipset_by_name_query(chipset_name)
                if chipset_data is None:
                    await send_protected_message(message, f"Bunday Nomli Chipset Mavjud Emas!")
                    return

                await send_protected_message(message, f"ID: {chipset_data['id']}\n"
                                     f"Name: {chipset_data['name']}\n"
                                     f"Created At: {chipset_data['created_at']}")
                await send_protected_message(message, "Chipset Deleted Successfully!")
                delete_chipset_query(chipset_data['id'])

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_chipset_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(F.text == "Show Chipsets")
async def show_chipsets(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            chipset_file_path = os.path.join(BASE_PATH, "chipsets.txt")

            chipsets = get_all_chipsets_query()
            if len(chipsets) == 0:
                await send_protected_message(message, "There are no Chipsets!")
                await before_chipset_management(message)
                return

            try:
                with open(chipset_file_path, "w") as f:
                    for chipset in chipsets:
                        f.write(f"ID: {chipset['id']}\n"
                                f"Name: {chipset['name']}\n"
                                f"Created At: {chipset['created_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(chipset_file_path):
                    cat = FSInputFile(chipset_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(chipset_file_path):
                    os.remove(chipset_file_path)

                await before_chipset_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(F.text == "Edit Chipset")
async def edit_chipset(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Chipset's Name:")
            await state.set_state(EditChipsetState.chipset_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(EditChipsetState.chipset_id)
async def edit_chipset_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                chipset_name = message.text
                chipset_data = get_chipset_by_name_query(chipset_name)
                if chipset_data is None:
                    await send_protected_message(message, f"Bunday Nomli Chipset Mavjud Emas!")
                    await before_chipset_management(message)
                    return

                await send_protected_message(message, f"ID: {chipset_data['id']}\n"
                                     f"Name: {chipset_data['name']}\n"
                                     f"Created At: {chipset_data['created_at']}")
                await send_protected_message(message, "Enter New Name for Chipset:")
                await state.set_state(EditChipsetState.chipset_new_name)
                await state.update_data(chipset_id=chipset_data['id'])

            except Exception as e:
                print(e)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_chipset.message(EditChipsetState.chipset_new_name)
async def edit_chipset_new_name(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                chipset_new_name = message.text
                chipset_data = get_chipset_by_name_query(chipset_new_name)
                if chipset_data is not None:
                    await send_protected_message(message, f"Bunday Nomli Chipset Mavjud!")
                    return

                state_data = await state.get_data()

                await send_protected_message(message, f"Chipset Updated Successfully!")
                update_chipset_query(state_data['chipset_id'], chipset_new_name)

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_chipset_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
