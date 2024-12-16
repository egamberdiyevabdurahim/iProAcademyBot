import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from buttons.for_admin import swap_helper_management_menu
from buttons.for_others import skip_menu
from queries.for_model import get_all_models_query, get_model_by_id_query
from queries.for_swap import insert_swap_query, get_swap_by_id_query, delete_swap_query, get_all_swaps_query, \
    update_swap_query
from queries.for_swap_photo import insert_swap_photo_query, get_swap_photos_by_swap_id_query, delete_swap_photo_query
from queries.for_users import get_user_by_telegram_id_query, get_user_by_id_query
from states.admin_state import AddSwapState, DeleteSwapState, EditSwapState
from utils.activity_maker import activity_maker
from utils.addititons import BUTTONS_AND_COMMANDS, BASE_PATH
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_admin_message, not_active_message, not_registered_message

router_for_swap = Router()


@router_for_swap.message(F.text == "Swap Helper Management")
async def before_swap_management(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            await send_protected_message(message, "Swap Helper Management", reply_markup=swap_helper_management_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(F.text == "Add Swap Helper")
async def add_swap_helper(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            models_data = get_all_models_query()
            if len(models_data) == 0:
                await send_protected_message(message, "No models found!")
                return

            full = ""
            for model in models_data:
                full += f"ID: {model['id']}\nName: {model['name']}\n\n"

            await send_protected_message(message, content=full)

            await send_protected_message(message, "Enter Model ID:")
            await state.set_state(AddSwapState.swap_model_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(AddSwapState.swap_model_id)
async def add_swap_model_id(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            swap_model_id = message.text
            if swap_model_id is None:
                await send_protected_message(message, "Model id cannot be empty!")
                await state.clear()
                return

            if swap_model_id in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Invalid model id!")
                await state.clear()
                return

            model_data = get_model_by_id_query(swap_model_id)
            if model_data is None:
                await send_protected_message(message, "Model not found!")
                await state.clear()
                return

            await send_protected_message(message, f"Model: {model_data['name']}")
            await state.update_data(swap_model_id=swap_model_id)
            await send_protected_message(message, f"Enter Title for Way:")
            await state.set_state(AddSwapState.swap_title)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(AddSwapState.swap_title)
async def add_swap_way_title(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_way_title = message.text
    if swap_way_title is None:
        await send_protected_message(message, "Title cannot be empty!")
        await state.clear()
        return

    if swap_way_title in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Invalid title!")
        await state.clear()
        return

    await state.update_data(swap_title=swap_way_title)

    await send_protected_message(message, "Enter Uz Name of Way:")
    await state.set_state(AddSwapState.swap_name_uz)


@router_for_swap.message(AddSwapState.swap_name_uz)
async def add_swap_way_uz_name(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_way_uz_name = message.text
    if swap_way_uz_name is None:
        await send_protected_message(message, "Uz Name cannot be empty!")
        await state.clear()
        return

    if swap_way_uz_name in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Invalid name!")
        await state.clear()
        return

    await state.update_data(swap_uz_name=swap_way_uz_name)
    await send_protected_message(message, "Enter Russian Name of Way:")
    await state.set_state(AddSwapState.swap_name_ru)


@router_for_swap.message(AddSwapState.swap_name_ru)
async def add_swap_way_ru_name(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_way_ru_name = message.text
    if swap_way_ru_name is None:
        await send_protected_message(message, "Russian Name cannot be empty!")
        await state.clear()
        return

    if swap_way_ru_name in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Invalid name!")
        await state.clear()
        return

    await state.update_data(swap_ru_name=swap_way_ru_name)
    await send_protected_message(message, "Enter English Name of Way:")
    await state.set_state(AddSwapState.swap_name_en)


@router_for_swap.message(AddSwapState.swap_name_en)
async def add_swap_way_en_name(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_way_en_name = message.text
    if swap_way_en_name is None:
        await send_protected_message(message, "English Name cannot be empty!")
        await state.clear()
        return

    if swap_way_en_name in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Invalid name!")
        await state.clear()
        return

    await state.update_data(swap_en_name=swap_way_en_name)

    await send_protected_message(message, "Send Photos as Group:")
    await state.set_state(AddSwapState.swap_photos)


@router_for_swap.message(AddSwapState.swap_photos)
async def add_swap_photo(message: Message, state: FSMContext):
    # If the message is a photo, process the photo
    if message.photo:
        media_items = message.photo
        # Get the highest quality photo by accessing the last item in message.photo
        highest_quality_photo = media_items[-1]  # Last item is the highest quality
        file_id = highest_quality_photo.file_id
        print(f"Photo file_id: {file_id}")

        # Store the photo in FSM state
        data = await state.get_data()
        if 'swap_photos' in data:
            data['swap_photos'].append(file_id)
        else:
            data['swap_photos'] = [file_id]

        # Update the state with new photo list
        await state.update_data(swap_photos=data['swap_photos'])

        # Prompt the user to continue or finish
        await send_protected_message(message, "Photo added. Send another photo or type 'Done' when finished.")

    # If the message is "Done", move to the next step
    elif message.text.lower() == 'done':
        # Retrieve all collected data
        data = await state.get_data()
        await state.clear()

        # Call the next step (finalizing the swap)
        await add_swap_end(message, data)

    else:
        await send_protected_message(message, "Please send photos or 'Done' to finish.")


@router_for_swap.message(AddSwapState.end)
async def add_swap_end(message: Message, data):
    swap_data = data
    user_id = get_user_by_telegram_id_query(message.from_user.id)['id']
    swap_model_id = swap_data['swap_model_id']
    swap_title = swap_data['swap_title']
    swap_name_uz = swap_data['swap_uz_name']
    swap_name_ru = swap_data['swap_ru_name']
    swap_name_en = swap_data['swap_en_name']
    swap_photos = swap_data.get('swap_photos', [])

    # Insert the swap information into the database
    swap_id = insert_swap_query(user_id=user_id,
                                model_id=swap_model_id,
                                title=swap_title,
                                name_uz=swap_name_uz,
                                name_ru=swap_name_ru,
                                name_en=swap_name_en)

    # Insert the photos into the database
    for photo in swap_photos:
        insert_swap_photo_query(swap_id=swap_id[0], photo_id=photo)

    # Confirmation message
    await send_protected_message(message, "Swap Helper added successfully!")

    await before_swap_management(message)


@router_for_swap.message(F.text=='Delete Swap Helper')
async def delete_swap_helper(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            await show_swap_helpers(message, True)
            await send_protected_message(message, "Enter Swap Helper ID to delete:")
            await state.set_state(DeleteSwapState.swap_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(DeleteSwapState.swap_id)
async def delete_swap_helper_id(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_id = message.text
    if swap_id is None:
        await send_protected_message(message, "Swap Helper ID cannot be empty!")
        await state.clear()
        return

    if not swap_id.isdigit():
        await send_protected_message(message, "Invalid Swap Helper ID!")
        await state.clear()
        return

    swap_data = get_swap_by_id_query(swap_id)
    if swap_data is None:
        await send_protected_message(message, "Swap Helper not found!")
        await state.clear()
        return

    await send_protected_message(message, f"Deleted Swap Helper: {swap_data['title']}")
    delete_swap_query(swap_id)
    await state.clear()
    await before_swap_management(message)


@router_for_swap.message(F.text=='Show Swap Helpers')
async def show_swap_helpers(message: Message, directed: bool=False):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            swap_file_path = os.path.join(BASE_PATH, "swap_helpers.txt")

            swaps = get_all_swaps_query()
            if len(swaps) == 0:
                await send_protected_message(message, "No swaps found.")
                await before_swap_management(message)
                return

            try:
                with open(swap_file_path, "w") as f:
                    for swap in swaps:
                        f.write(f"ID: {swap['id']}\n"
                                f"Title: {swap['title']}\n"
                                f"Name UZ: {swap['name_uz']}\n"
                                f"Name RU: {swap['name_ru']}\n"
                                f"Name EN: {swap['name_en']}\n"
                                f"User: {get_user_by_id_query(swap['user_id'])['first_name']}\n"
                                f"Created At: {swap['created_at']}\n"
                                f"Updated At: {swap['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(swap_file_path):
                    cat = FSInputFile(swap_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")
            finally:
                # Clean up the file after sending
                if os.path.exists(swap_file_path):
                    os.remove(swap_file_path)

                if directed is False:
                    await before_swap_management(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(F.text=='Edit Swap Helper')
async def edit_swap_helper(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                await state.clear()
                return

            swap_file_path = os.path.join(BASE_PATH, "swap_helpers.txt")

            swaps = get_all_swaps_query()
            if len(swaps) == 0:
                await send_protected_message(message, "No swaps found.")
                await before_swap_management(message)
                return

            try:
                with open(swap_file_path, "w") as f:
                    for swap in swaps:
                        f.write(f"ID: {swap['id']}\n"
                                f"Title: {swap['title']}\n"
                                f"Name UZ: {swap['name_uz']}\n"
                                f"Name RU: {swap['name_ru']}\n"
                                f"Name EN: {swap['name_en']}\n"
                                f"User: {get_user_by_id_query(swap['user_id'])['first_name']}\n"
                                f"Created At: {swap['created_at']}\n"
                                f"Updated At: {swap['updated_at']}\n"
                                f"{'-' * 20}\n")

                if os.path.exists(swap_file_path):
                    cat = FSInputFile(swap_file_path)
                    await send_protected_message(message, document=cat)
                else:
                    await send_protected_message(message, "The file does not exist.")

            except Exception as e:
                await send_protected_message(message, f"An error occurred: {e}")

            if os.path.exists(swap_file_path):
                os.remove(swap_file_path)

            await send_protected_message(message, "Enter swap ID:")
            await state.set_state(EditSwapState.swap_id)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@router_for_swap.message(EditSwapState.swap_id)
async def edit_swap_helper_id(message: Message, state: FSMContext):
    await activity_maker(message)

    swap_id = message.text
    if swap_id is None:
        await send_protected_message(message, "Swap ID cannot be empty!")
        await state.clear()
        await before_swap_management(message)
        return

    if swap_id in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Invalid!")
        await state.clear()
        await before_swap_management(message)
        return

    if not swap_id.isdigit():
        await send_protected_message(message, "Invalid Swap ID!")
        await state.clear()
        await before_swap_management(message)
        return

    swap_data = get_swap_by_id_query(swap_id)
    if swap_data is None:
        await send_protected_message(message, "Swap Helper not found!")
        await state.clear()
        await before_swap_management(message)
        return

    await send_protected_message(message, "Enter new title:", reply_markup=skip_menu)
    await state.update_data(swap_id=swap_id)
    await state.set_state(EditSwapState.swap_new_title)


@router_for_swap.message(EditSwapState.swap_new_title)
async def edit_swap_helper_new_title(message: Message, state: FSMContext):
    await activity_maker(message)

    new_title = message.text
    if new_title == "Skip":
        new_title = None

    else:
        if new_title is None:
            await send_protected_message(message, "New title cannot be empty!")
            await state.clear()
            await before_swap_management(message)
            return

        if new_title in BUTTONS_AND_COMMANDS:
            await send_protected_message(message, "Invalid!")
            await state.clear()
            await before_swap_management(message)
            return

    models_data = get_all_models_query()
    if len(models_data) == 0:
        await send_protected_message(message, "No models found!")
        return

    full = ""
    for model in models_data:
        full += f"ID: {model['id']}\nName: {model['name']}\n\n"

    await send_protected_message(message, content=full)

    await state.update_data(swap_new_title=new_title)
    await send_protected_message(message, "Enter new model ID:", reply_markup=skip_menu)
    await state.set_state(EditSwapState.swap_new_model_id)


@router_for_swap.message(EditSwapState.swap_new_model_id)
async def edit_swap_helper_new_model_id(message: Message, state: FSMContext):
    await activity_maker(message)

    new_model_id = message.text
    if new_model_id == "Skip":
        new_model_id = None

    else:
        if new_model_id is None:
            await send_protected_message(message, "New model ID cannot be empty!")
            await state.clear()
            await before_swap_management(message)
            return

        if not new_model_id.isdigit():
            await send_protected_message(message, "Invalid model ID!")
            await state.clear()
            await before_swap_management(message)
            return

    await state.update_data(swap_new_model_id=new_model_id)
    await send_protected_message(message, "Enter new name UZ:", reply_markup=skip_menu)
    await state.set_state(EditSwapState.swap_new_name_uz)


@router_for_swap.message(EditSwapState.swap_new_name_uz)
async def edit_swap_helper_new_name_uz(message: Message, state: FSMContext):
    await activity_maker(message)

    new_name_uz = message.text
    if new_name_uz == "Skip":
        new_name_uz = None

    else:
        if new_name_uz is None:
            await send_protected_message(message, "New name UZ cannot be empty!")
            await state.clear()
            await before_swap_management(message)
            return

        if new_name_uz in BUTTONS_AND_COMMANDS:
            await send_protected_message(message, "Invalid!")
            await state.clear()
            await before_swap_management(message)
            return

    await state.update_data(swap_new_name_uz=new_name_uz)
    await send_protected_message(message, "Enter new name RU:", reply_markup=skip_menu)
    await state.set_state(EditSwapState.swap_new_name_ru)


@router_for_swap.message(EditSwapState.swap_new_name_ru)
async def edit_swap_helper_new_name_ru(message: Message, state: FSMContext):
    await activity_maker(message)

    new_name_ru = message.text
    if new_name_ru == "Skip":
        new_name_ru = None

    else:
        if new_name_ru is None:
            await send_protected_message(message, "New name RU cannot be empty!")
            await state.clear()
            await before_swap_management(message)
            return

        if new_name_ru in BUTTONS_AND_COMMANDS:
            await send_protected_message(message, "Invalid!")
            await state.clear()
            await before_swap_management(message)
            return

    await state.update_data(swap_new_name_ru=new_name_ru)
    await send_protected_message(message, "Enter new name EN:", reply_markup=skip_menu)
    await state.set_state(EditSwapState.swap_new_name_en)


@router_for_swap.message(EditSwapState.swap_new_name_en)
async def edit_swap_helper_new_name_en(message: Message, state: FSMContext):
    await activity_maker(message)

    new_name_en = message.text
    if new_name_en == "Skip":
        new_name_en = None

    else:
        if new_name_en is None:
            await send_protected_message(message, "New name EN cannot be empty!")
            await state.clear()
            await before_swap_management(message)
            return

        if new_name_en in BUTTONS_AND_COMMANDS:
            await send_protected_message(message, "Invalid!")
            await state.clear()
            await before_swap_management(message)
            return

    await state.update_data(swap_new_name_en=new_name_en)
    await send_protected_message(message, "Send new photos:", reply_markup=skip_menu)
    await state.set_state(EditSwapState.swap_photos)


@router_for_swap.message(EditSwapState.swap_photos)
async def edit_swap_helper_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.photo:
        media_items = message.photo
        # Get the highest quality photo by accessing the last item in message.photo
        highest_quality_photo = media_items[-1]  # Last item is the highest quality
        file_id = highest_quality_photo.file_id
        print(f"Photo file_id: {file_id}")

        # Store the photo in FSM state
        if 'swap_photos' in data:
            data['swap_photos'].append(file_id)
        else:
            data['swap_photos'] = [file_id]

        # Update the state with new photo list
        await state.update_data(swap_photos=data['swap_photos'])

        # Prompt the user to continue or finish
        await send_protected_message(message, "Photo added. Send another photo or type 'Done' when finished.")

    # If the message is "Done", move to the next step
    elif message.text == "Skip":
        await state.update_data(swap_photos=None)
        await state.clear()
        await edit_swap_end(message, data)

    elif message.text.lower() == 'done':
        # Retrieve all collected data
        await state.clear()

        # Call the next step (finalizing the swap)
        await edit_swap_end(message, data)

    else:
        await send_protected_message(message, "Please send photos or 'Done' to finish.")


async def edit_swap_end(message: Message, data):
    swap_data = data
    swap_id = swap_data['swap_id']
    org_swap_data = get_swap_by_id_query(swap_id)
    swap_model_id = swap_data.get('swap_new_model_id')
    swap_title = swap_data.get('swap_new_title')
    swap_name_uz = swap_data.get('swap_new_name_uz')
    swap_name_ru = swap_data.get('swap_new_name_ru')
    swap_name_en = swap_data.get('swap_new_name_en')
    swap_photos = swap_data.get('swap_photos', [])

    if swap_model_id is None:
        swap_model_id = org_swap_data['model_id']

    if swap_title is None:
        swap_title = org_swap_data['title']

    if swap_name_uz is None:
        swap_name_uz = org_swap_data['name_uz']

    if swap_name_ru is None:
        swap_name_ru = org_swap_data['name_ru']

    if swap_name_en is None:
        swap_name_en = org_swap_data['name_en']

    # Insert the swap information into the database
    update_swap_query(swap_id=swap_id,
                      model_id=swap_model_id,
                      title=swap_title,
                      name_uz=swap_name_uz,
                      name_ru=swap_name_ru,
                      name_en=swap_name_en)

    if len(swap_photos) > 0:
        old_photos = get_swap_photos_by_swap_id_query(swap_id)
        for photo in old_photos:
            delete_swap_photo_query(swap_photo_id=photo['id'])
            print("deleting")

        for photo in swap_photos:
            insert_swap_photo_query(swap_id=swap_id, photo_id=photo)
            print("adding")

    # Confirmation message
    await send_protected_message(message, "Swap Helper edited successfully!")
    await send_protected_message(message, f"Model ID: {swap_model_id}\n"
                                          f"Title: {swap_title}\n"
                                          f"Name UZ: {swap_name_uz}\n"
                                          f"Name RU: {swap_name_ru}\n"
                                          f"Name EN: {swap_name_en}\n", media_group=swap_photos)

    await before_swap_management(message)