from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from buttons.for_user import i2c_menu
from queries.for_chipset import get_chipset_by_name_query
from queries.for_i2c import get_i2c_by_category_and_chipset_query
from queries.for_i2c_category import get_i2c_category_by_name_query
from queries.for_users import get_user_by_telegram_id_query
from states.user_states import I2CState
from user.user.user_handlers import i2c_go
from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, is_active, not_active_message

user_i2c_router = Router()

@user_i2c_router.message(I2CState.to_category)
async def i2c_to_category_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await state.update_data(to_category=get_i2c_category_by_name_query(message.text)['id'])

            if await i2c_menu(message.text):
                await send_protected_message(message, f"{message.text}", reply_markup=await i2c_menu(message.text))
                await state.set_state(I2CState.to_chipset)

            else:
                await i2c_go(message, state)

        else:
            await not_active_message(message)


@user_i2c_router.message(I2CState.to_chipset)
async def i2c_to_chipset_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            state_data = await state.get_data()

            chipset_id = get_chipset_by_name_query(message.text)

            if chipset_id is None:
                await i2c_go(message, state)
                return None

            data = get_i2c_by_category_and_chipset_query(category_id=state_data['to_category'], chipset_id=chipset_id['id'])
            user_language = get_user_by_telegram_id_query(message.from_user.id)['language_code']

            if data is None:
                await i2c_go(message, state)
                return None

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