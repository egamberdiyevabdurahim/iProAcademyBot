from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.for_user import panic_menu
from queries.for_panic import get_all_panics_query, get_panic_by_code_query
from queries.for_panic_array import get_all_panic_arrays_query, get_panic_array_by_id_query
from queries.for_users import get_user_by_telegram_id_query
from states.user_states import PanicState
from user.user.user_handlers import panic_go
from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, is_active, not_active_message

user_panic_router = Router()


@user_panic_router.message(F.text == "🔙Back To Array")
async def back_to_array(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await panic_array_go(message, state)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_panic_router.message(PanicState.to_array)
async def panic_array_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            # Fetch all panic array names
            panic_arrays = [data['name'] for data in get_all_panic_arrays_query()]

            # Check if the message text matches one of the panic array names
            if message.text in panic_arrays:
                await send_protected_message(message, f"{message.text}", reply_markup=await panic_menu(message.text))
                await state.set_state(PanicState.after_array)

            else:
                await panic_go(message, state)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_panic_router.message(PanicState.after_array)
async def panic_sender(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            panic_datas = [data['code'] for data in get_all_panics_query()]
            user_language = get_user_by_telegram_id_query(message.from_user.id)
            if message.text in panic_datas:
                panic_data = get_panic_by_code_query(message.text)
                if user_language['language_code'] == 'uz':
                    await send_protected_message(message, f"{panic_data['name_uz']}")

                elif user_language['language_code'] == 'ru':
                    await send_protected_message(message, f"{panic_data['name_ru']}")

                else:
                    await send_protected_message(message, f"{panic_data['name_en']}")

            await state.clear()
            await state.set_state(PanicState.after_array)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)