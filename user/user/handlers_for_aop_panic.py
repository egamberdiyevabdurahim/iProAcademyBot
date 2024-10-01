from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from queries.for_aop_panic import get_aop_panic_by_code_query
from queries.for_users import get_user_by_telegram_id_query
from states.user_states import AOPPanicState
from user.user.user_handlers import aop_panic_go
from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, is_active, not_active_message

user_aop_panic_router = Router()


@user_aop_panic_router.message(AOPPanicState.to_data)
async def user_aop_panic_data_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            data = get_aop_panic_by_code_query(message.text)
            user_language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if data is None:
                await aop_panic_go(message, state)

            else:
                if user_language == "uz":
                    await send_protected_message(message, data['name_uz'])

                elif user_language == "ru":
                    await send_protected_message(message, data['name_ru'])

                else:
                    await send_protected_message(message, data['name_en'])

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)