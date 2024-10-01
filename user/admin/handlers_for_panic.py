import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import panic_management_menu
from queries.for_panic import get_panic_by_code_query, insert_panic_query, delete_panic_query, \
    get_all_panics_query
from queries.for_panic_array import get_all_panic_arrays_query, get_panic_array_by_id_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddPanicState, DeletePanicState
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_panic = Router()


@router_for_panic.message(F.text == "Panic Management")
async def panic_management_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Panic Management", reply_markup=panic_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(F.text == "Add Panic")
async def add_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Panic's Code:")
            await state.set_state(AddPanicState.panic_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(AddPanicState.panic_code)
async def add_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_code = message.text
                panic_data = get_panic_by_code_query(panic_code)
                if panic_data is not None:
                    await send_protected_message(message, f"Bu Codeli Panic Mavjud!")
                    await panic_management_go(message)
                    return

                await state.update_data(panic_code=panic_code)
                await send_protected_message(message, "Enter Panic's Uzbek Name:")
                await state.set_state(AddPanicState.panic_name_uz)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(AddPanicState.panic_name_uz)
async def add_panic_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_name_uz = message.text
                await state.update_data(panic_name_uz=panic_name_uz)

                await send_protected_message(message, "Enter Panic's Russian Name:")
                await state.set_state(AddPanicState.panic_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(AddPanicState.panic_name_ru)
async def add_panic_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_name_ru = message.text
                await state.update_data(panic_name_ru=panic_name_ru)

                await send_protected_message(message, "Enter Panic's English Name:")
                await state.set_state(AddPanicState.panic_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(AddPanicState.panic_name_en)
async def add_panic_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_name = message.text
                await state.update_data(panic_name_en=panic_name)

                panic_array_data = get_all_panic_arrays_query()
                if panic_array_data is None:
                    await send_protected_message(message, "Panic Array Topilmadi\n"
                                         "Avval Panic Array Qo'shing!")
                    await panic_management_go(message)
                    return

                for panic_array in panic_array_data:
                    await send_protected_message(message, f"ID:{panic_array['id']}. Name:{panic_array['name']}")

                await send_protected_message(message, "Enter Panic Array ID:")
                await state.set_state(AddPanicState.panic_array_id)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(AddPanicState.panic_array_id)
async def add_panic_array_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_array_id = message.text
                panic_array_data = get_panic_array_by_id_query(int(panic_array_id))
                if panic_array_data is None:
                    await send_protected_message(message, "Bu IDli Panic Array Mavjud Emas!")
                    await panic_management_go(message)
                    return

                await state.update_data(panic_array_id=panic_array_id)

                state_data = await state.get_data()
                panic_name_uz = state_data['panic_name_uz']
                panic_name_ru = state_data['panic_name_ru']
                panic_name_en = state_data['panic_name_en']
                panic_code = state_data['panic_code']
                panic_array_id = state_data['panic_array_id']
                user_data = get_user_by_telegram_id_query(message.from_user.id)

                insert_panic_query(array_id=panic_array_id,
                                   name_uz=panic_name_uz,
                                   name_ru=panic_name_ru,
                                   name_en=panic_name_en,
                                   code=panic_code,
                                   user_id=user_data['id'])
                await send_protected_message(message, f"Panic {panic_name_uz} created successfully!")

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(F.text == "Delete Panic")
async def delete_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Panic's Code:")
            await state.set_state(DeletePanicState.panic_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(DeletePanicState.panic_id)
async def delete_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                panic_code = message.text
                panic_data = get_panic_by_code_query(panic_code)
                if panic_data is None:
                    await send_protected_message(message, f"Bu Codeli Panic Mavjud Emas!")
                    return

                await send_protected_message(message, f"ID: {panic_data['id']}\n"
                                     f"Name UZ: {panic_data['name_uz']}\n"
                                     f"Name RU: {panic_data['name_ru']}\n"
                                     f"Name EN: {panic_data['name_en']}\n"
                                     f"Code: {panic_data['code']}\n"
                                     f"Array: {get_panic_array_by_id_query(panic_data['array_id'])['name']}\n"
                                     f"User: {get_user_by_id_query(panic_data['user_id'])['first_name']}\n"
                                     f"Created At: {panic_data['created_at']}\n"
                                     f"Updated At: {panic_data['updated_at']}")

                panic_id = panic_data['id']
                delete_panic_query(panic_id)
                await send_protected_message(message, "Panic Deleted Successfully!")

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(F.text == "Show Panics")
async def show_panics(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            panic_file_path = os.path.join(BASE_PATH, "panic.txt")

            panics = get_all_panics_query()
            if len(panics) == 0:
                await send_protected_message(message, "Panics not found.")
                await panic_management_go(message)
                return

            try:
                with open(panic_file_path, "w") as f:
                    for panic in panics:
                        f.write(f"ID: {panic['id']}\n"
                                f"Name UZ: {panic['name_uz']}\n"
                                f"Name RU: {panic['name_ru']}\n"
                                f"Name EN: {panic['name_en']}\n"
                                f"Code: {panic['code']}\n"
                                f"Array: {get_panic_array_by_id_query(panic['array_id'])['name']}\n"
                                f"User: {get_user_by_id_query(panic['user_id'])['first_name']}\n"
                                f"Created At: {panic['created_at']}\n"
                                f"Updated At: {panic['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(panic_file_path):
                    cat = FSInputFile(panic_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                # Clean up the file after sending
                if os.path.exists(panic_file_path):
                    os.remove(panic_file_path)

                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(F.text == "Edit Panic")
async def edit_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Coming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
