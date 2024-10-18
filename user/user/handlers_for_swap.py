from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, ReplyKeyboardMarkup

from buttons.for_user import model_menu

from queries.for_model import get_model_by_name_query
from queries.for_swap import get_swap_by_title_and_model_id_query
from queries.for_swap_photo import get_swap_photos_by_swap_id_query
from queries.for_users import get_user_by_telegram_id_query

from states.user_states import SwapState

from user.user.user_handlers import swap_go

from utils.activity_maker import activity_maker
from utils.addititons import BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_active_message, not_registered_message

user_swap_router = Router()


@user_swap_router.message(SwapState.to_data)
async def models_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if message.text in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Try Again!")
                await state.clear()
                return

            markup = await model_menu(message.text, language)

            if markup is not None and isinstance(markup, ReplyKeyboardMarkup):
                model_data = get_model_by_name_query(message.text)
                await state.update_data(to_data=model_data)
                await send_protected_message(message, f"{message.text}:", reply_markup=markup)
                await state.set_state(SwapState.end)
            else:
                await send_protected_message(message, "Coming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_swap_router.message(SwapState.end)
async def swap_data_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            try:
                if message.text in BUTTONS_AND_COMMANDS:
                    await state.clear()
                    return

                state_data = await state.get_data()
                model_id = state_data['to_data']['id']

                data = get_swap_by_title_and_model_id_query(model_id=model_id, title=message.text)
                if data is None:
                    await send_protected_message(message, "Coming Soon🔥")
                    await state.clear()
                    await swap_go(message, state)

                language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
                if language == 'uz':
                    await swap_data_sender(message, language, data)

                elif language == 'ru':
                    await swap_data_sender(message, language, data)

                else:
                    await swap_data_sender(message, language, data)

                await state.set_state(SwapState.end)

            except Exception:
                pass

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


async def swap_data_sender(message: Message, language, data):
    photos = get_swap_photos_by_swap_id_query(data['id'])
    photos_data = list()

    # Use the saved Telegram file IDs directly in InputMediaPhoto
    for photo in photos:
        photos_data.append(InputMediaPhoto(media=photo['photo_id']))

    # Send the media group
    await message.answer_media_group(photos_data, protect_content=True)

    # Send the appropriate language message
    if language == "uz":
        await send_protected_message(message, content=data['name_uz'])
    elif language == "ru":
        await send_protected_message(message, content=data['name_ru'])
    elif language == "en":
        await send_protected_message(message, content=data['name_en'])
