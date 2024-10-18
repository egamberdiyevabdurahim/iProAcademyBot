from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from queries.for_itunes import get_itunes_by_error_code_query
from queries.for_users import get_user_by_telegram_id_query
from states.user_states import ITunesState
from utils.addititons import BUTTONS_AND_COMMANDS
from utils.proteceds import send_protected_message

user_itunes_router = Router()


@user_itunes_router.message(ITunesState.to_data)
async def user_itunes_data_go(message: Message, state: FSMContext):
    if message.text in BUTTONS_AND_COMMANDS:
        await send_protected_message(message, "Try Again!")
        await state.clear()
        return

    language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
    data = get_itunes_by_error_code_query(message.text)
    if data is None:
        await send_protected_message(message, f"Error code {message.text} not found.")

    if language == 'uz':
        await send_protected_message(message, content=data['name_uz'])

    elif language == 'ru':
        await send_protected_message(message, content=data['name_ru'])

    else:
        await send_protected_message(message, content=data['name_en'])

    await state.clear()
    await state.set_state(ITunesState.to_data)
