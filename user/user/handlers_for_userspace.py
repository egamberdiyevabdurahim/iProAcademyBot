from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from queries.for_users import get_user_by_telegram_id_query
from queries.for_userspace import get_userspace_by_code_query
from states.user_states import UserSpaceState
from user.user.user_handlers import userspace_go
from utils.activity_maker import activity_maker
from utils.addititons import BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, is_active, not_active_message

user_userspace_router = Router()


@user_userspace_router.message(UserSpaceState.to_data)
async def user_space_data_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            if message.text in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, "Try Again!")
                await state.clear()
                return

            data = get_userspace_by_code_query(message.text)
            user_language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if data is not None:
                if user_language == "uz":
                    await send_protected_message(message, data['name_uz'])

                elif user_language == "ru":
                    await send_protected_message(message, data['name_ru'])

                else:
                    await send_protected_message(message, data['name_en'])

            else:
                await userspace_go(message, state)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)