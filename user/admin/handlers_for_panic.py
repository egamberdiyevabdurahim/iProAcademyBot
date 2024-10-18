import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import panic_management_menu
from buttons.for_others import skip_menu
from queries.for_panic import get_panic_by_code_query, insert_panic_query, delete_panic_query, \
    get_all_panics_query, get_panic_by_id_query, update_panic_query
from queries.for_panic_array import get_all_panic_arrays_query, get_panic_array_by_id_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddPanicState, DeletePanicState, EditPanicState
from utils.activity_maker import activity_maker

from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
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
                if panic_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                panic_data = get_panic_by_code_query(panic_code)
                if panic_data is not None:
                    await send_protected_message(message, f"Bu Codeli Panic Mavjud!")
                    await state.clear()
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
                if panic_name_uz in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

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
                if panic_name_ru in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

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
                if panic_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                await state.update_data(panic_name_en=panic_name)

                panic_array_data = get_all_panic_arrays_query()
                if panic_array_data is None:
                    await send_protected_message(message, "Panic Array Topilmadi\n"
                                         "Avval Panic Array Qo'shing!")
                    await state.clear()
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
                if panic_array_id in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

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
                if panic_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

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

            if os.path.exists(panic_file_path):
                os.remove(panic_file_path)

            await send_protected_message(message, "Enter Panic ID:")
            await state.set_state(EditPanicState.panic_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_id)
async def edit_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                panic_id = int(message.text)
                panic_data = get_panic_by_id_query(panic_id)
                if panic_data is None:
                    await send_protected_message(message, "Bu IDli Panic Mavjud Emas!")
                    await state.clear()
                    await panic_management_go(message)
                    return

                await send_protected_message(message, f"Enter new name uz:", reply_markup=skip_menu)
                await state.update_data(panic_id=panic_id)
                await state.set_state(EditPanicState.panic_new_name_uz)

            except ValueError:
                await send_protected_message(message, "ID must be a number!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_new_name_uz)
async def edit_panic_new_name_uz(message: Message, state: FSMContext):
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
                    if len(new_name_uz) == 0:
                        await send_protected_message(message, "Name bo'sh bo'lish olmaslig'i lovim etdingiz!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                    if new_name_uz in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                await send_protected_message(message, "Enter new name Ru:", reply_markup=skip_menu)
                await state.update_data(new_name_uz=new_name_uz)
                await state.set_state(EditPanicState.panic_new_name_ru)

            except Exception as e:
                print(str(e))
                await send_protected_message(message, "Xatolik yuz berdi!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_new_name_ru)
async def edit_panic_new_name_ru(message: Message, state: FSMContext):
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
                    if len(new_name_ru) == 0:
                        await send_protected_message(message, "Name bo'sh bo'lish olmaslig'i lovim etdingiz!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                    if new_name_ru in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                await send_protected_message(message, "Enter new name EN:", reply_markup=skip_menu)
                await state.update_data(new_name_ru=new_name_ru)
                await state.set_state(EditPanicState.panic_new_name_en)

            except Exception as e:
                print(str(e))
                await send_protected_message(message, "Xatolik yuz berdi!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_new_name_en)
async def edit_panic_new_name_en(message: Message, state: FSMContext):
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
                    if len(new_name_en) == 0:
                        await send_protected_message(message, "Name bo'sh bo'lish olmaslig'i lovim etdingiz!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                    if new_name_en in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                panic_array_file_path = os.path.join(BASE_PATH, "panic_arrays.txt")

                panic_arrays = get_all_panic_arrays_query()
                if len(panic_arrays) == 0:
                    await send_protected_message(message, "No Panic Arrays Found!")
                    await state.clear()
                    await panic_management_go(message)
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
                        await state.clear()
                        await panic_management_go(message)

                except Exception as e:
                    await send_protected_message(message, f"An error occurred: {e}")
                    await state.clear()
                    await panic_management_go(message)

                if os.path.exists(panic_array_file_path):
                    os.remove(panic_array_file_path)

                await send_protected_message(message, "Enter panic array ID:", reply_markup=skip_menu)
                await state.update_data(panic_new_name_en=new_name_en)
                await state.set_state(EditPanicState.panic_array_id)

            except Exception as e:
                print(str(e))
                await send_protected_message(message, "Xatolik yuz berdi!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_array_id)
async def edit_panic_array_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                panic_id = message.text
                if panic_id == "Skip":
                    panic_id = None

                else:
                    panic_array = get_panic_array_by_id_query(panic_id)
                    if panic_array is None:
                        await send_protected_message(message, "Bu IDli Panic Array Mavjud Emas!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                    if panic_id in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                await send_protected_message(message, f"Enter new code:", reply_markup=skip_menu)
                await state.update_data(panic_array_id=panic_id)
                await state.set_state(EditPanicState.panic_new_code)

            except Exception as e:
                print(str(e))
                await send_protected_message(message, "Xatolik yuz berdi!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_panic.message(EditPanicState.panic_new_code)
async def edit_panic_new_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                new_code = message.text
                if new_code == "Skip":
                    new_code = None

                else:
                    if len(new_code) == 0:
                        await send_protected_message(message, "Code bo'sh bo'lish olmaslig'i lovim etdingiz!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                    if new_code in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        await panic_management_go(message)
                        return

                state_data = await state.get_data()
                panic_id = state_data.get("panic_id")
                new_name_uz = state_data.get("panic_new_name_uz")
                new_name_ru = state_data.get("panic_new_name_ru")
                new_name_en = state_data.get("panic_new_name_en")
                panic_array_id = state_data.get("panic_array_id")

                panic_data = get_panic_by_id_query(panic_id)

                if new_name_uz is None:
                    new_name_uz = panic_data['name_uz']

                if new_name_ru is None:
                    new_name_ru = panic_data['name_ru']

                if new_name_en is None:
                    new_name_en = panic_data['name_en']

                if panic_array_id is None:
                    panic_array_id = panic_data['array_id']

                update_panic_query(panic_id=panic_id,
                                   new_name_uz=new_name_uz,
                                   new_name_ru=new_name_ru,
                                   new_name_en=new_name_en,
                                   array_id=panic_array_id,
                                   code=new_code)

                await send_protected_message(message, "Panic array updated successfully!")
                await state.clear()
                await panic_management_go(message)

            except Exception as e:
                print(str(e))
                await send_protected_message(message, "Xatolik yuz berdi!")
                await state.clear()
                await panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
