import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile


from buttons.for_admin import array_management_menu
from queries.for_panic_array import get_panic_array_by_name_query, insert_panic_array_query, delete_panic_array_query, \
    update_panic_array_name_query, get_all_panic_arrays_query
from queries.for_users import get_user_by_telegram_id_query

from states.admin_state import AddPanicArrayState, DeletePanicArrayState, EditPanicArrayState
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_panic_array = Router()


@router_for_panic_array.message(F.text == "Panic Array Management")
async def before_panic_array_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Array Management", reply_markup=array_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(F.text == "Add Panic Array")
async def add_panic_array(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Panic Array's Name:")
            await state.set_state(AddPanicArrayState.panic_array_name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(AddPanicArrayState.panic_array_name)
async def add_panic_array_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_array_name = message.text
                panic_array_data = get_panic_array_by_name_query(panic_array_name)
                if panic_array_data is not None:
                    await send_protected_message(message, f"Bunday Nomli Panic Array Mavjud!")
                    return

                await send_protected_message(message, "Panic Array Created Successfully!")
                insert_panic_array_query(panic_array_name)

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_panic_array_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(F.text == "Delete Panic Array")
async def delete_panic_array(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Panic Array's Name:")
            await state.set_state(DeletePanicArrayState.panic_array_name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(DeletePanicArrayState.panic_array_name)
async def delete_panic_array_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_array_name = message.text
                panic_array_data = get_panic_array_by_name_query(panic_array_name)
                if panic_array_data is None:
                    await send_protected_message(message, f"Bunday Nomli Panic Array Mavjud emas!")
                    return

                await send_protected_message(message, f"ID:{panic_array_data['id']}\n"
                                                      f"Name:{panic_array_data['name']}\n"
                                                      f"Created At:{panic_array_data['created_at']}")

                await send_protected_message(message, "Panic Array Deleted Successfully!")
                delete_panic_array_query(panic_array_data['id'])

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_panic_array_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(F.text == "Edit Panic Array")
async def edit_panic_array(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Panic Array's Name:")
            await state.set_state(EditPanicArrayState.panic_array_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(EditPanicArrayState.panic_array_id)
async def edit_panic_array_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_array_name = message.text
                panic_array_data = get_panic_array_by_name_query(panic_array_name)
                if panic_array_data is None:
                    await send_protected_message(message, f"Bunday Nomli Panic Array Mavjud emas!")
                    await before_panic_array_management(message)
                    return

                await send_protected_message(message, f"Current Panic Array Name: {panic_array_data['name']}\n"
                                     f"Enter New Panic Array's Name:")
                await state.update_data(panic_array_id=panic_array_data['id'])
                await state.set_state(EditPanicArrayState.panic_array_new_name)

            except Exception as e:
                print(e)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(EditPanicArrayState.panic_array_new_name)
async def edit_panic_array_new_name(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_array_new_name = message.text
                panic_array_data = get_panic_array_by_name_query(panic_array_new_name)
                if panic_array_data is not None:
                    await send_protected_message(message, f"Bunday Nomli Panic Array Allaqachon Mavjud!")
                    return

                panic_array_id = await state.get_data()
                await send_protected_message(message, "Panic Array Updated Successfully!")
                update_panic_array_name_query(panic_array_id=panic_array_id['panic_array_id'], new_name=panic_array_new_name)

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_panic_array_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic_array.message(F.text == "Show Panic Arrays")
async def show_panic_arrays(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            panic_array_file_path = os.path.join(BASE_PATH, "panic_arrays.txt")

            panic_arrays = get_all_panic_arrays_query()
            if len(panic_arrays) == 0:
                await send_protected_message(message, "No Panic Arrays Found!")
                await before_panic_array_management(message)
                return

            try:
                with open(panic_array_file_path, "w") as f:
                    for panic_array in panic_arrays:
                        f.write(f"ID: {panic_array['id']}\n"
                                f"Name: {panic_array['name']}\n"
                                f"Created At: {panic_array['created_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(panic_array_file_path):
                    cat = FSInputFile(panic_array_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(panic_array_file_path):
                    os.remove(panic_array_file_path)

                await before_panic_array_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
