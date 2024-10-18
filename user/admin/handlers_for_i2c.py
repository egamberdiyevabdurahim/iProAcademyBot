import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import i2c_management_menu
from buttons.for_others import skip_menu
from queries.for_chipset import get_all_chipsets_query, get_chipset_by_id_query
from queries.for_i2c import insert_i2c_query, delete_i2c_query, get_all_i2cs_query, get_i2c_by_name_uz_query, \
    get_i2c_by_name_ru_query, get_i2c_by_name_en_query, get_i2c_by_category_and_chipset_query, get_i2c_by_id_query, \
    update_i2c_query
from queries.for_i2c_category import get_all_i2c_categories_query, get_i2c_category_by_id_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddI2CState, DeleteI2CState, EditI2CState
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_i2c = Router()


@router_for_i2c.message(F.text == "i2c Management")
async def i2c_management_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "i2c Management", reply_markup=i2c_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(F.text == "Add i2c")
async def add_i2c(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter i2c's Uzbek Name:")
            await state.set_state(AddI2CState.i2c_name_uz)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(AddI2CState.i2c_name_uz)
async def add_i2c_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                i2c_name = message.text
                if i2c_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                if i2c_name is None:
                    await send_protected_message(message, "I2c Uzbek Name Bo'sh Bo'lishi Mumkin Emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                await state.update_data(i2c_name_uz=i2c_name)

                await send_protected_message(message, "Enter i2c's Russian Name:")
                await state.set_state(AddI2CState.i2c_name_ru)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(AddI2CState.i2c_name_ru)
async def add_i2c_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                i2c_name = message.text
                if i2c_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                if i2c_name is None:
                    await send_protected_message(message, "I2c Russian Name Bo'sh Bo'lishi Mumkin Emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                await state.update_data(i2c_name_ru=i2c_name)

                await send_protected_message(message, "Enter i2c's English Name:")
                await state.set_state(AddI2CState.i2c_name_en)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(AddI2CState.i2c_name_en)
async def add_i2c_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                i2c_name = message.text
                if i2c_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                if i2c_name is None:
                    await send_protected_message(message, "I2c English Name Bo'sh Bo'lishi Mumkin Emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                await state.update_data(i2c_name_en=i2c_name)

                chipset_datas = get_all_chipsets_query()
                for chipset in chipset_datas:
                    await send_protected_message(message, f"ID: {chipset['id']}. Name:{chipset['name']}")

                await send_protected_message(message, "Enter Chipset ID:")
                await state.set_state(AddI2CState.chipset_id)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(AddI2CState.chipset_id)
async def add_i2c_chipset_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                chipset_id = message.text

                if not chipset_id.isnumeric():
                    await send_protected_message(message, "Bu IDli Chipset Mavjud Emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                chipset_data = get_chipset_by_id_query(int(chipset_id))
                if chipset_data is None:
                    await send_protected_message(message, "Bu IDli Chipset Mavjud Emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                await state.update_data(chipset_id=chipset_id)

                i2c_category_datas = get_all_i2c_categories_query()
                for i2c_category in i2c_category_datas:
                    await send_protected_message(message, f"ID: {i2c_category['id']}. Name:{i2c_category['name']}")

                await send_protected_message(message, "Enter i2c Category ID:")
                await state.set_state(AddI2CState.category_id)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(AddI2CState.category_id)
async def add_i2c_category_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                category_id = message.text
                if not category_id.isnumeric():
                    await send_protected_message(message, "Bu IDli i2c Category Mavjud Emas!")
                    await state.clear()
                    return

                category_data = get_i2c_category_by_id_query(int(category_id))
                if category_data is None:
                    await send_protected_message(message, "Bu IDli i2c Category Mavjud Emas!")
                    await state.clear()
                    return

                await state.update_data(category_id=category_id)
                state_data = await state.get_data()
                i2c_name_uz = state_data['i2c_name_uz']
                i2c_name_ru = state_data['i2c_name_ru']
                i2c_name_en = state_data['i2c_name_en']
                chipset_id = state_data['chipset_id']
                category_id = state_data['category_id']
                user_id = get_user_by_telegram_id_query(message.from_user.id)['id']

                allowed_data = get_i2c_by_category_and_chipset_query(category_id=category_id, chipset_id=chipset_id)
                if allowed_data is not None:
                    await send_protected_message(message, "Bu kategoriyada bu chipsetda i2c mavjud bo'lishi mumkin!")
                    await state.clear()
                    return

                await send_protected_message(message, f"i2c {i2c_name_uz} created successfully!")

                insert_i2c_query(name_uz=i2c_name_uz,
                                 name_ru=i2c_name_ru,
                                 name_en=i2c_name_en,
                                 chipset_id=chipset_id,
                                 category_id=category_id,
                                 user_id=user_id)

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await i2c_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(F.text == "Delete i2c")
async def delete_i2c(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            i2c_file_path = os.path.join(BASE_PATH, "i2c.txt")

            i2cs = get_all_i2cs_query()
            if len(i2cs) == 0:
                await send_protected_message(message, "No i2c found!")
                await i2c_management_go(message)
                return

            try:
                with open(i2c_file_path, "w") as f:
                    for i2c in i2cs:
                        f.write(f"ID: {i2c['id']}\n"
                                f"Name UZ: {i2c['name_uz']}\n"
                                f"Name RU: {i2c['name_ru']}\n"
                                f"Name EN: {i2c['name_en']}\n"
                                f"Chipset: {get_chipset_by_id_query(i2c['chipset_id'])['name']}\n"
                                f"Category: {get_i2c_category_by_id_query(i2c['category_id'])['name']}\n"
                                f"User: {get_user_by_id_query(i2c['user_id'])['first_name']}\n"
                                f"Created At: {i2c['created_at']}\n"
                                f"Updated At: {i2c['updated_at']}\n"
                                f"{'-' * 20}\n")
                if os.path.exists(i2c_file_path):
                    cat = FSInputFile(i2c_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
                await state.clear()
                await i2c_management_go(message)

            if os.path.exists(i2c_file_path):
                os.remove(i2c_file_path)

            await send_protected_message(message, "Enter i2c's ID:")
            await state.set_state(DeleteI2CState.i2c_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(DeleteI2CState.i2c_id)
async def delete_i2c_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                i2c_name = message.text.strip()  # Strip any leading/trailing spaces
                if i2c_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                i2c_data = get_i2c_by_id_query(i2c_name)

                if i2c_data is None:
                    await send_protected_message(message, "Bunday i2c mavjud emas!")  # I2C not found
                    return

                # Fetch related data (chipset, category, user)
                chipset = get_chipset_by_id_query(i2c_data['chipset_id'])
                category = get_i2c_category_by_id_query(i2c_data['category_id'])
                user = get_user_by_telegram_id_query(i2c_data['user_id'])

                # Respond with I2C information
                await send_protected_message(message, f"ID: {i2c_data['id']}\n"
                                     f"Name UZ: {i2c_data['name_uz']}\n"
                                     f"Name RU: {i2c_data['name_ru']}\n"
                                     f"Name EN: {i2c_data['name_en']}\n"
                                     f"Chipset: {chipset['name'] if chipset else 'N/A'}\n"
                                     f"Category: {category['name'] if category else 'N/A'}\n"
                                     f"User: {get_user_by_id_query(i2c_data['user_id'])['first_name']}\n"
                                     f"Created At: {i2c_data['created_at']}\n"
                                     f"Updated At: {i2c_data['updated_at']}")

                # Delete I2C entry
                delete_i2c_query(i2c_data['id'])

                # Confirm deletion
                await send_protected_message(message, "i2c successfully deleted!")

            except Exception as e:
                print(f"Error deleting i2c: {str(e)}")
                await send_protected_message(message, "Xatolik yuz berdi! I2C ni o'chirishda muammo bor.")  # Error deleting I2C

            finally:
                await state.clear()
                await i2c_management_go(message)  # Redirect to I2C management

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(F.text == "Show i2cs")
async def show_i2cs(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            i2c_file_path = os.path.join(BASE_PATH, "i2c.txt")

            i2cs = get_all_i2cs_query()
            if len(i2cs) == 0:
                await send_protected_message(message, "No i2c found!")
                await i2c_management_go(message)
                return

            try:
                with open(i2c_file_path, "w") as f:
                    for i2c in i2cs:
                        f.write(f"ID: {i2c['id']}\n"
                                f"Name UZ: {i2c['name_uz']}\n"
                                f"Name RU: {i2c['name_ru']}\n"
                                f"Name EN: {i2c['name_en']}\n"
                                f"Chipset: {get_chipset_by_id_query(i2c['chipset_id'])['name']}\n"
                                f"Category: {get_i2c_category_by_id_query(i2c['category_id'])['name']}\n"
                                f"User: {get_user_by_id_query(i2c['user_id'])['first_name']}\n"
                                f"Created At: {i2c['created_at']}\n"
                                f"Updated At: {i2c['updated_at']}\n"
                                f"{'-' * 20}\n")
                if os.path.exists(i2c_file_path):
                    cat = FSInputFile(i2c_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(i2c_file_path):
                    os.remove(i2c_file_path)

                await i2c_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(F.text == "Edit i2c")
async def edit_i2c(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            i2c_file_path = os.path.join(BASE_PATH, "i2c.txt")

            i2cs = get_all_i2cs_query()
            if len(i2cs) == 0:
                await send_protected_message(message, "No i2c found!")
                await i2c_management_go(message)
                return

            try:
                with open(i2c_file_path, "w") as f:
                    for i2c in i2cs:
                        f.write(f"ID: {i2c['id']}\n"
                                f"Name UZ: {i2c['name_uz']}\n"
                                f"Name RU: {i2c['name_ru']}\n"
                                f"Name EN: {i2c['name_en']}\n"
                                f"Chipset: {get_chipset_by_id_query(i2c['chipset_id'])['name']}\n"
                                f"Category: {get_i2c_category_by_id_query(i2c['category_id'])['name']}\n"
                                f"User: {get_user_by_id_query(i2c['user_id'])['first_name']}\n"
                                f"Created At: {i2c['created_at']}\n"
                                f"Updated At: {i2c['updated_at']}\n"
                                f"{'-' * 20}\n")
                if os.path.exists(i2c_file_path):
                    cat = FSInputFile(i2c_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
                await state.clear()
                await i2c_management_go(message)

            if os.path.exists(i2c_file_path):
                os.remove(i2c_file_path)

            await send_protected_message(message, "Enter i2c ID:")
            await state.set_state(EditI2CState.i2c_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.i2c_id)
async def edit_i2c_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            i2c_id = message.text
            if i2c_id is None or not i2c_id.isnumeric():
                await send_protected_message(message, "I2c ID bo'sh bo'lishi mumkin emas!")
                await state.clear()
                await i2c_management_go(message)
                return

            i2c_data = get_i2c_by_id_query(int(i2c_id))
            if i2c_data is None:
                await send_protected_message(message, "Bunday i2c mavjud emas!")
                await state.clear()
                await i2c_management_go(message)
                return

            await send_protected_message(message, f"Enter new name Uz", reply_markup=skip_menu)
            await state.update_data(i2c_id=i2c_id)
            await state.set_state(EditI2CState.i2c_new_name_uz)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.i2c_new_name_uz)
async def edit_i2c_new_name_uz(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            new_name_uz = message.text
            if new_name_uz == 'Skip':
                new_name_uz = None

            else:
                if new_name_uz in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            await state.update_data(i2c_new_name_uz=new_name_uz)
            await send_protected_message(message, f"Enter new name Ru", reply_markup=skip_menu)
            await state.set_state(EditI2CState.i2c_new_name_ru)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.i2c_new_name_ru)
async def edit_i2c_new_name_ru(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            new_name_ru = message.text
            if new_name_ru == 'Skip':
                new_name_ru = None

            else:
                if new_name_ru in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            await state.update_data(i2c_new_name_ru=new_name_ru)
            await send_protected_message(message, f"Enter new name En", reply_markup=skip_menu)
            await state.set_state(EditI2CState.i2c_new_name_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.i2c_new_name_en)
async def edit_i2c_new_name_en(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            new_name_en = message.text
            if new_name_en == 'Skip':
                new_name_en = None

            else:
                if new_name_en in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            chipset_file_path = os.path.join(BASE_PATH, "chipsets.txt")

            chipsets = get_all_chipsets_query()
            if len(chipsets) == 0:
                await send_protected_message(message, "There are no Chipsets!")
                await state.clear()
                await i2c_management_go(message)
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
                await state.clear()
                await i2c_management_go(message)

            if os.path.exists(chipset_file_path):
                os.remove(chipset_file_path)

            await state.update_data(i2c_new_name_en=new_name_en)
            await send_protected_message(message, "Enter new chipset ID:", reply_markup=skip_menu)
            await state.set_state(EditI2CState.chipset_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.chipset_id)
async def edit_chipset_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            chipset_id = message.text
            if chipset_id == 'Skip':
                chipset_id = None

            else:
                if chipset_id in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                chipset_data = get_chipset_by_id_query(chipset_id)
                if chipset_data is None:
                    await send_protected_message(message, "Bunday chipset mavjud emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            i2c_categories_file_path = os.path.join(BASE_PATH, "i2c_categories.txt")

            i2c_categories = get_all_i2c_categories_query()
            if len(i2c_categories) == 0:
                await send_protected_message(message, "No i2c Categories found.")
                await state.clear()
                await i2c_management_go(message)
                return

            try:
                with open(i2c_categories_file_path, "w") as file:
                    for category in i2c_categories:
                        file.write(f"ID: {category['id']}\n"
                                   f"Name: {category['name']}\n"
                                   f"Created At: {category['created_at']}\n\n")

                await send_protected_message(message, document=FSInputFile(i2c_categories_file_path))

            except Exception as e:
                print(str(e))
                await state.clear()
                await i2c_management_go(message)

            if os.path.exists(i2c_categories_file_path):
                os.remove(i2c_categories_file_path)

            await send_protected_message(message, f"Enter new description Uz", reply_markup=skip_menu)
            await state.update_data(chipset_id=chipset_id)
            await state.set_state(EditI2CState.category_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c.message(EditI2CState.category_id)
async def edit_category_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await i2c_management_go(message)
                return

            category_id = message.text
            if category_id == 'Skip':
                category_id = None

            else:
                if category_id in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

                category_data = get_i2c_category_by_id_query(category_id)
                if category_data is None:
                    await send_protected_message(message, "Bunday idlik kategoriya mavjud emas!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            state_data = await state.get_data()
            i2c_id = state_data.get("i2c_id")
            i2c_new_name_uz = state_data.get('i2c_new_name_uz')
            i2c_new_name_ru = state_data.get('i2c_new_name_ru')
            i2c_new_name_en = state_data.get('i2c_new_name_en')
            chipset_id = state_data.get('chipset_id')

            i2c_data = get_i2c_by_id_query(i2c_id)

            skip1 = False
            skip2 = False
            if i2c_new_name_uz is None:
                i2c_new_name_uz = i2c_data['name_uz']

            if i2c_new_name_ru is None:
                i2c_new_name_ru = i2c_data['name_ru']

            if i2c_new_name_en is None:
                i2c_new_name_en = i2c_data['name_en']

            if chipset_id is None:
                skip1 = True
                chipset_id = i2c_data['chipset_id']

            if category_id is None:
                skip2 = True
                category_id = i2c_data['category_id']

            if not skip1 and not skip2:
                if get_i2c_by_category_and_chipset_query(category_id, chipset_id) is not None:
                    await send_protected_message(message, "Bunday idlik kategoriya va chipset mavjud!")
                    await state.clear()
                    await i2c_management_go(message)
                    return

            update_i2c_query(id_of=i2c_id,
                             new_name_uz=i2c_new_name_uz,
                             new_name_ru=i2c_new_name_ru,
                             new_name_en=i2c_new_name_en,
                             chipset_id=chipset_id,
                             category_id=category_id,
                             user_id=user_data['id'])

            await send_protected_message(message, "I2C updated successfully!")
            await state.clear()
            await i2c_management_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
