import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import aop_panic_management_menu
from buttons.for_others import skip_menu
from queries.for_aop_panic import get_aop_panic_by_code_query, insert_aop_panic_query, delete_aop_panic_query, \
    get_all_aop_panics_query, update_aop_panic_query, get_aop_panic_by_id_query
from queries.for_panic_array import get_panic_array_by_id_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddAopPanicState, DeleteAopPanicState, EditAopPanicState
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_aop_panic = Router()


@router_for_aop_panic.message(F.text == "AOP Panic Management")
async def aop_panic_management_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "AOP Panic Management", reply_markup=aop_panic_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(F.text == "Add AOP Panic")
async def add_aop_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter AOP Panic's Code:")
            await state.set_state(AddAopPanicState.aop_panic_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(AddAopPanicState.aop_panic_code)
async def add_aop_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                aop_panic_code = message.text
                if aop_panic_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                aop_panic_data = get_aop_panic_by_code_query(aop_panic_code)
                if aop_panic_data is not None:
                    await send_protected_message(message, f"Bu Codeli AOP Panic Mavjud!")
                    await state.clear()
                    return

                await state.update_data(aop_panic_code=aop_panic_code)

                await send_protected_message(message, "Enter AOP Panic's Uzbek Name:")
                await state.set_state(AddAopPanicState.aop_panic_name_uz)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(AddAopPanicState.aop_panic_name_uz)
async def add_aop_panic_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                aop_panic_name = message.text
                if aop_panic_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                await state.update_data(aop_panic_name_uz=aop_panic_name)

                await send_protected_message(message, "Enter AOP Panic's Russian Name:")
                await state.set_state(AddAopPanicState.aop_panic_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(AddAopPanicState.aop_panic_name_ru)
async def add_aop_panic_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                aop_panic_name = message.text
                if aop_panic_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                await state.update_data(aop_panic_name_ru=aop_panic_name)

                await send_protected_message(message, "Enter AOP Panic's English Name:")
                await state.set_state(AddAopPanicState.aop_panic_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(AddAopPanicState.aop_panic_name_en)
async def add_aop_panic_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                aop_panic_name = message.text
                if aop_panic_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                await state.update_data(aop_panic_name_en=aop_panic_name)

                state_data = await state.get_data()
                aop_panic_code = state_data['aop_panic_code']
                aop_panic_name_uz = state_data['aop_panic_name_uz']
                aop_panic_name_ru = state_data['aop_panic_name_ru']
                aop_panic_name_en = state_data['aop_panic_name_en']
                user_id = get_user_by_telegram_id_query(message.from_user.id)['id']

                await send_protected_message(message, f"AOP Panic {aop_panic_name} created successfully!")

                insert_aop_panic_query(code=aop_panic_code,
                                       name_uz=aop_panic_name_uz,
                                       name_ru=aop_panic_name_ru,
                                       name_en=aop_panic_name_en,
                                       user_id=user_id)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await aop_panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(F.text == "Delete AOP Panic")
async def delete_aop_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter AOP Panic's Code:")
            await state.set_state(DeleteAopPanicState.aop_panic_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(DeleteAopPanicState.aop_panic_id)
async def delete_aop_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                aop_panic_code = message.text
                if aop_panic_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                aop_panic_data = get_aop_panic_by_code_query(aop_panic_code)
                if aop_panic_data is None:
                    await send_protected_message(message, f"Bunday Codeli AOP Panic Mavjud Emas!")
                    return

                await send_protected_message(message, f"AOP Panic {aop_panic_code} deleted successfully!")

                delete_aop_panic_query(aop_panic_data['id'])

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await aop_panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(F.text == "Show AOP Panics")
async def show_aop_panics(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            aop_panic_file_path = os.path.join(BASE_PATH, "aop_panic.txt")

            aop_panics = get_all_aop_panics_query()
            if len(aop_panics) == 0:
                await send_protected_message(message, "There are no AOP Panics!")
                await aop_panic_management_go(message)
                return

            try:
                with open(aop_panic_file_path, "w") as f:
                    for aop_panic in aop_panics:
                        f.write(f"ID: {aop_panic['id']}\n"
                                f"Name UZ: {aop_panic['name_uz']}\n"
                                f"Name RU: {aop_panic['name_ru']}\n"
                                f"Name EN: {aop_panic['name_en']}\n"
                                f"Code: {aop_panic['code']}\n"
                                f"User: {get_user_by_id_query(aop_panic['user_id'])['first_name']}\n"
                                f"Created At: {aop_panic['created_at']}\n"
                                f"Updated At: {aop_panic['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(aop_panic_file_path):
                    cat = FSInputFile(aop_panic_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(aop_panic_file_path):
                    os.remove(aop_panic_file_path)

                await aop_panic_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(F.text == "Edit AOP Panic")
async def edit_aop_panic(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            await send_protected_message(message, "Enter AOP Panic's Code:")
            await state.set_state(EditAopPanicState.aop_panic_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(EditAopPanicState.aop_panic_id)
async def edit_aop_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                aop_panic_code = message.text
                if aop_panic_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                aop_panic_data = get_aop_panic_by_code_query(aop_panic_code)
                if aop_panic_data is None:
                    await send_protected_message(message, f"Bunday Codeli AOP Panic Mavjud Emas!")
                    await state.clear()
                    return

                await send_protected_message(message, "Enter new name Uz:", reply_markup=skip_menu)
                await state.update_data(aop_panic_id=aop_panic_data['id'])
                await state.set_state(EditAopPanicState.panic_name_uz)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)



@router_for_aop_panic.message(EditAopPanicState.panic_name_uz)
async def edit_panic_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                name_uz = message.text
                if name_uz == 'Skip':
                    name_uz = None

                else:
                    if name_uz in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        return

                await send_protected_message(message, "Enter new name Ru:", reply_markup=skip_menu)
                await state.update_data(panic_name_uz=name_uz)
                await state.set_state(EditAopPanicState.panic_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(EditAopPanicState.panic_name_ru)
async def edit_panic_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                name_ru = message.text
                if name_ru == 'Skip':
                    name_ru = None

                else:
                    if name_ru in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        return

                await send_protected_message(message, "Enter new name En:", reply_markup=skip_menu)
                await state.update_data(panic_name_ru=name_ru)
                await state.set_state(EditAopPanicState.panic_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)



@router_for_aop_panic.message(EditAopPanicState.panic_name_en)
async def edit_panic_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            try:
                name_en = message.text
                if name_en == 'Skip':
                    name_en = None

                else:
                    if name_en in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        return

                await send_protected_message(message, "Enter new code", reply_markup=skip_menu)
                await state.update_data(panic_name_en=name_en)
                await state.set_state(EditAopPanicState.panic_code)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_aop_panic.message(EditAopPanicState.panic_code)
async def edit_panic_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                code = message.text
                if code == 'Skip':
                    code = None

                else:
                    if code in BUTTONS_AND_COMMANDS:
                        await send_protected_message(message, "Invalid!")
                        await state.clear()
                        return

                    aop_panic_data = get_aop_panic_by_code_query(code)
                    if aop_panic_data is not None:
                        await send_protected_message(message, f"Bunday Codeli AOP Panic Mavjud!")
                        await state.clear()
                        return

                state_data = await state.get_data()
                panic_name_uz = state_data.get('panic_name_uz')
                panic_name_ru = state_data.get('panic_name_ru')
                panic_name_en = state_data.get('panic_name_en')
                panic_id = state_data.get('aop_panic_id')

                panic_data = get_aop_panic_by_id_query(panic_id)
                if panic_name_uz is None:
                    panic_name_uz = panic_data['name_uz']

                if panic_name_ru is None:
                    panic_name_ru = panic_data['name_ru']

                if panic_name_en is None:
                    panic_name_en = panic_data['name_en']

                if code is None:
                    code = panic_data['code']

                update_aop_panic_query(id_of=panic_id,
                                       new_name_uz=panic_name_uz,
                                       new_name_ru=panic_name_ru,
                                       new_name_en=panic_name_en,
                                       code=code)
                await send_protected_message(message, f"Bunday Codeli AOP Panic {code} Muvaffaqiyatli O'zgartirildi!")
                await state.clear()
                await aop_panic_management_go(message)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)

