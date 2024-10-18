import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import i2c_category_management_menu
from queries.for_i2c_category import insert_i2c_category_query, get_i2c_category_by_name_query, \
    delete_i2c_category_query, get_all_i2c_categories_query, update_i2c_category_query
from queries.for_users import get_user_by_telegram_id_query
from states.admin_state import AddI2CCategoryState, \
    DeleteI2CCategoryState, EditI2CCategoryState
from utils.activity_maker import activity_maker
from utils.addititons import BASE_PATH, BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

router_for_i2c_category = Router()


@router_for_i2c_category.message(F.text == "i2c Category Management")
async def before_i2c_category_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "i2c Category Management", reply_markup=i2c_category_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(F.text == "Add i2c Category")
async def add_i2c_category(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter i2c Category's Name:")
            await state.set_state(AddI2CCategoryState.category_name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(AddI2CCategoryState.category_name)
async def add_i2c_category_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                category_name = message.text
                if category_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                category_data = get_i2c_category_by_name_query(category_name)
                if category_data is not None:
                    await send_protected_message(message, "This i2c Category already exists.")

                insert_i2c_category_query(category_name)
                await send_protected_message(message, f"i2c Category '{category_name}' added successfully.")

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await before_i2c_category_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(F.text == "Delete i2c Category")
async def delete_i2c_category(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter i2c Category's Name:")
            await state.set_state(DeleteI2CCategoryState.category_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(DeleteI2CCategoryState.category_id)
async def delete_i2c_category_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                category_name = message.text
                if category_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                category_data = get_i2c_category_by_name_query(category_name)
                if category_data is None:
                    await send_protected_message(message, "This i2c Category does not exist.")
                    return

                await send_protected_message(message, f"ID: {category_data['id']}\n"
                                     f"Name: {category_data['name']}\n"
                                     f"Created At: {category_data['created_at']}")

                delete_i2c_category_query(category_data['id'])
                await send_protected_message(message, f"i2c Category '{category_name}' deleted successfully.")

            except Exception as e:
                print(str(e))

            finally:
                await state.clear()
                await before_i2c_category_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(F.text == "Show i2c Categories")
async def show_i2cs(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            i2c_categories_file_path = os.path.join(BASE_PATH, "i2c_categories.txt")

            i2c_categories = get_all_i2c_categories_query()
            if len(i2c_categories) == 0:
                await send_protected_message(message, "No i2c Categories found.")
                await before_i2c_category_management(message)
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

            finally:
                if os.path.exists(i2c_categories_file_path):
                    os.remove(i2c_categories_file_path)

                await before_i2c_category_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(F.text == "Edit i2c Category")
async def edit_i2c_category(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter i2c Category's Name:")
            await state.set_state(EditI2CCategoryState.category_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(EditI2CCategoryState.category_id)
async def edit_i2c_category_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                category_name = message.text
                if category_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    await state.clear()
                    return

                category_data = get_i2c_category_by_name_query(category_name)
                if category_data is None:
                    await send_protected_message(message, "This i2c Category does not exist.")
                    await state.clear()
                    await before_i2c_category_management(message)
                    return

                await send_protected_message(message, f"ID: {category_data['id']}\n"
                                     f"Name: {category_data['name']}\n"
                                     f"Created At: {category_data['created_at']}")

                await state.update_data(category_id=category_data['id'])

                await send_protected_message(message, "Enter New Name:")
                await state.set_state(EditI2CCategoryState.category_new_name)

            except Exception as e:
                print(str(e))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_i2c_category.message(EditI2CCategoryState.category_new_name)
async def edit_i2c_category_new_name(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            try:
                i2c_category_new_name = message.text
                if i2c_category_new_name in BUTTONS_AND_COMMANDS:
                    await send_protected_message(message, "Invalid!")
                    return

                i2c_category_data = get_i2c_category_by_name_query(i2c_category_new_name)
                if i2c_category_data is not None:
                    await send_protected_message(message, f"Bunday Nomli i2c Category Mavjud!")
                    return

                state_data = await state.get_data()

                await send_protected_message(message, f"Chipset Updated Successfully!")
                update_i2c_category_query(state_data['category_id'], i2c_category_new_name)

            except Exception as e:
                print(e)

            finally:
                await state.clear()
                await before_i2c_category_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)

