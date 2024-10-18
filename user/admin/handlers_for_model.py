import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import model_management_menu
from queries.for_model import insert_model_query, delete_model_query, get_model_by_name_query, get_all_models_query, \
    update_model_query
from queries.for_users import get_user_by_telegram_id_query
from states.admin_state import AddModelState, DeleteModelState, EditModelState
from utils.activity_maker import activity_maker
from utils.addititons import BUTTONS_AND_COMMANDS, BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_admin_message, not_active_message, not_registered_message

router_for_model = Router()


@router_for_model.message(F.text == "Model Management")
async def before_model_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Model Management", reply_markup=model_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(F.text == "Add Model")
async def add_model(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Model's Name:")
            await state.set_state(AddModelState.name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(AddModelState.name)
async def add_model_name(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await state.clear()

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return
            model_name = message.text
            if model_name is None:
                await send_protected_message(message, "Name must be non empty!")
                return

            if model_name in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                return

            insert_model_query(model_name)
            await send_protected_message(message, f"Model '{model_name}' added successfully.")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(F.text == "Delete Model")
async def delete_model(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Model's Name:")
            await state.set_state(DeleteModelState.model_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(DeleteModelState.model_id)
async def delete_model_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await state.clear()

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            model_name = message.text
            if model_name is None:
                await send_protected_message(message, "ID must be non empty!")
                return

            if model_name in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                return

            model_data = get_model_by_name_query(model_name)
            if model_data is None:
                await send_protected_message(message, f"Model with ID '{model_name}' does not exist.")
                return

            delete_model_query(model_data['id'])
            await send_protected_message(message, f"Model with ID '{model_name}' deleted successfully.")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(F.text == "Show Models")
async def show_models(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            model_file_path = os.path.join(BASE_PATH, "models.txt")

            models = get_all_models_query()
            if len(models) == 0:
                await send_protected_message(message, "No Model Found!")
                await before_model_management(message)
                return

            try:
                with open(model_file_path, "w") as f:
                    for model in models:
                        f.write(f"ID: {model['id']}\n"
                                f"Name: {model['name']}\n"
                                f"Created At: {model['created_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(model_file_path):
                    cat = FSInputFile(model_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(model_file_path):
                    os.remove(model_file_path)

                await before_model_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(F.text == "Edit Model")
async def edit_model_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Enter Model's Name:")
            await state.set_state(EditModelState.model_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(EditModelState.model_id)
async def edit_model_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            await state.clear()

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            model_name = message.text
            if model_name is None:
                await send_protected_message(message, "ID must be non empty!")
                await state.clear()
                return

            if model_name in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            model_data = get_model_by_name_query(model_name)
            if model_data is None:
                await send_protected_message(message, f"Model with ID '{model_name}' does not exist.")
                await state.clear()
                return

            await state.update_data(model_id=model_data['id'])

            await send_protected_message(message, f"Model with Name '{model_name}' found. Enter new name:")
            await state.set_state(EditModelState.new_name)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_model.message(EditModelState.new_name)
async def edit_model_name(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            state_data = await state.get_data()
            model_id = state_data.get('model_id')
            new_name = message.text
            if new_name is None:
                await send_protected_message(message, "New Name must be non empty!")
                await state.clear()
                return

            if new_name in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid!")
                await state.clear()
                return

            update_model_query(model_id, new_name)
            await send_protected_message(message, f"Model with ID '{model_id}' updated successfully. New Name: {new_name}")
            await state.clear()
            await before_model_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)