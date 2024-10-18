import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import alphabet_management_menu
from buttons.for_others import skip_menu
from queries.for_alphabets import get_alphabet_by_code_query, insert_alphabet_query, \
    delete_alphabet_query, get_all_alphabets_query, get_alphabet_by_id_query, update_alphabet_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddAlphabetState, DeleteAlphabetState, EditAlphabetState
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_alphabets = Router()


@router_for_alphabets.message(F.text == "Alphabet Management")
async def before_alphabet_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Alphabet Management", reply_markup=alphabet_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(F.text == "Add Alphabet")
async def add_alphabet(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Alphabet's Code:")
            await state.set_state(AddAlphabetState.alphabet_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(AddAlphabetState.alphabet_code)
async def add_alphabet_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_code = message.text
                if alphabet_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                alphabet_data = get_alphabet_by_code_query(alphabet_code)
                if alphabet_data is not None:
                    await send_protected_message(message, f"Bu Codeli Alphabet Mavjud!")
                    await state.clear()
                    return

                await state.update_data(alphabet_code=alphabet_code)

                await send_protected_message(message, "Enter Alphabet's Uzbek Name:")
                await state.set_state(AddAlphabetState.alphabet_name_uz)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(AddAlphabetState.alphabet_name_uz)
async def add_alphabet_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_name = message.text
                if alphabet_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                await state.update_data(alphabet_name_uz=alphabet_name)

                await send_protected_message(message, "Enter Alphabet's Russian Name:")
                await state.set_state(AddAlphabetState.alphabet_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(AddAlphabetState.alphabet_name_ru)
async def add_alphabet_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_name = message.text
                if alphabet_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                await state.update_data(alphabet_name_ru=alphabet_name)

                await send_protected_message(message, "Enter Alphabet's English Name:")
                await state.set_state(AddAlphabetState.alphabet_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(AddAlphabetState.alphabet_name_en)
async def add_alphabet_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_name = message.text
                if alphabet_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                await state.update_data(alphabet_name_en=alphabet_name)

                state_data = await state.get_data()
                alphabet_code = state_data['alphabet_code']
                alphabet_name_uz = state_data['alphabet_name_uz']
                alphabet_name_ru = state_data['alphabet_name_ru']
                alphabet_name_en = state_data['alphabet_name_en']
                user_id = get_user_by_telegram_id_query(message.from_user.id)['id']

                await send_protected_message(message, f"Alphabet {alphabet_name} created successfully!")

                insert_alphabet_query(code=alphabet_code,
                                      name_uz=alphabet_name_uz,
                                      name_ru=alphabet_name_ru,
                                      name_en=alphabet_name_en,
                                      user_id=user_id)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await before_alphabet_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(F.text == "Delete Alphabet")
async def delete_alphabet(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Alphabet's Code:")
            await state.set_state(DeleteAlphabetState.alphabet_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(DeleteAlphabetState.alphabet_id)
async def delete_alphabet_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_code = message.text
                if alphabet_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                alphabet_data = get_alphabet_by_code_query(alphabet_code)
                if alphabet_data is None:
                    await send_protected_message(message, f"Bunday Codeli Alphabet Mavjud Emas!")
                    return

                alphabet_id = alphabet_data['id']

                await send_protected_message(message, f"Alphabet with ID {alphabet_id} deleted successfully!")

                delete_alphabet_query(alphabet_id)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await before_alphabet_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(F.text == "Show Alphabets")
async def show_alphabets(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            alphabet_file_path = os.path.join(BASE_PATH, "alphabet.txt")

            alphabets = get_all_alphabets_query()
            if len(alphabets) == 0:
                await send_protected_message(message, "No alphabets found.")
                await before_alphabet_management(message)
                return

            try:
                with open(alphabet_file_path, "w") as f:
                    for alphabet in alphabets:
                        f.write(f"ID: {alphabet['id']}\n"
                                f"Name UZ: {alphabet['name_uz']}\n"
                                f"Name RU: {alphabet['name_ru']}\n"
                                f"Name EN: {alphabet['name_en']}\n"
                                f"Code: {alphabet['code']}\n"
                                f"User: {get_user_by_id_query(alphabet['user_id'])['first_name']}\n"
                                f"Created At: {alphabet['created_at']}\n"
                                f"Updated At: {alphabet['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(alphabet_file_path):
                    cat = FSInputFile(alphabet_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(alphabet_file_path):
                    os.remove(alphabet_file_path)

                await before_alphabet_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(F.text == "Edit Alphabet")
async def edit_alphabet(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Alphabet's Code:")
            await state.set_state(EditAlphabetState.alphabet_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(EditAlphabetState.alphabet_id)
async def edit_alphabet_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_code = message.text
                if alphabet_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                alphabet_data = get_alphabet_by_code_query(alphabet_code)
                if alphabet_data is None:
                    await send_protected_message(message, f"Bunday Codeli Alphabet Mavjud Emas!")
                    await state.clear()
                    return

                alphabet_id = alphabet_data['id']
                await state.update_data(alphabet_id=alphabet_id)

                await send_protected_message(message, f"Enter uzbek name:", reply_markup=skip_menu)
                await state.set_state(EditAlphabetState.alphabet_new_name_uz)

            except Exception as e:
                print(str(e))
                await state.clear()

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(EditAlphabetState.alphabet_new_name_uz)
async def edit_alphabet_new_name_uz(message: Message, state: FSMContext):
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
                        return

                await state.update_data(alphabet_new_name_uz=new_name_uz)
                await send_protected_message(message, f"Enter russian name:", reply_markup=skip_menu)
                await state.set_state(EditAlphabetState.alphabet_new_name_ru)

            except Exception as e:
                print(str(e))
                await state.clear()

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(EditAlphabetState.alphabet_new_name_ru)
async def edit_alphabet_new_name_ru(message: Message, state: FSMContext):
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
                        return

                await state.update_data(alphabet_new_name_ru=new_name_ru)
                await send_protected_message(message, f"Enter english name:", reply_markup=skip_menu)
                await state.set_state(EditAlphabetState.alphabet_new_name_en)

            except Exception as e:
                print(str(e))
                await state.clear()

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(EditAlphabetState.alphabet_new_name_en)
async def edit_alphabet_new_name_en(message: Message, state: FSMContext):
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
                        return

                await state.update_data(alphabet_new_name_en=new_name_en)
                await send_protected_message(message, "Enter new code:", reply_markup=skip_menu)
                await state.set_state(EditAlphabetState.alphabet_new_code)

            except Exception as e:
                print(str(e))
                await state.clear()

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_alphabets.message(EditAlphabetState.alphabet_new_code)
async def edit_alphabet_new_code(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                alphabet_code = message.text
                if alphabet_code == "Skip":
                    alphabet_code = None
                if alphabet_code in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                state_data = await state.get_data()
                alphabet_id = state_data['alphabet_id']
                alphabet_name_uz = state_data['alphabet_new_name_uz']
                alphabet_name_ru = state_data['alphabet_new_name_ru']
                alphabet_name_en = state_data['alphabet_new_name_en']

                alphabet_real_data = get_alphabet_by_id_query(alphabet_id)

                if alphabet_code is not None:
                    alphabet_data = get_alphabet_by_code_query(alphabet_code)
                    if alphabet_data['code'] == alphabet_code and alphabet_data['id'] != alphabet_id:
                        await send_protected_message(message, "This code is already exists!")
                        return

                else:
                    alphabet_code = alphabet_real_data['code']

                if not alphabet_name_uz:
                    alphabet_name_uz = alphabet_real_data['name_uz']

                if not alphabet_name_ru:
                    alphabet_name_ru = alphabet_real_data['name_ru']

                if not alphabet_name_en:
                    alphabet_name_en = alphabet_real_data['name_en']

                print("aaaaaa")

                update_alphabet_query(alphabet_id=alphabet_id,
                                      new_code=alphabet_code,
                                      new_name_uz=alphabet_name_uz,
                                      new_name_ru=alphabet_name_ru,
                                      new_name_en=alphabet_name_en)

                await send_protected_message(message, "Alphabet successfully edited\n"
                                                      "Edited data:\n"
                                                      f"Code: {alphabet_code}\n"
                                                      f"Name UZ: {alphabet_name_uz}\n"
                                                      f"Name RU: {alphabet_name_ru}\n"
                                                      f"Name EN: {alphabet_name_en}")

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await before_alphabet_management(message)
