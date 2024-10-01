from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from buttons.for_user import main_menu_first_uz, main_menu_first_ru, main_menu_first_en
from queries.for_pending_users import delete_pending_user_by_telegram_id_query
from queries.for_users import insert_user_query
from states.auth_state import RegisterState
from buttons.for_auth import share_number_uz, share_number_rus, share_number_eng
from utils.proteceds import send_protected_message

router = Router()

# Helper function to send language-specific main menu
async def send_main_menu(message: Message, language_code: str):
    if language_code == 'uz':
        await send_protected_message(message, "Menyu:", reply_markup=main_menu_first_uz)
    elif language_code == 'ru':
        await send_protected_message(message, "Меню:", reply_markup=main_menu_first_ru)
    else:
        await send_protected_message(message, "Menu:", reply_markup=main_menu_first_en)


@router.message(RegisterState.phone_number)
async def register_number(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()

        # Validate required data
        if not all(key in state_data for key in ('language_code', 'first_name', 'last_name', 'telegram_id')):
            await message.answer("Some required data is missing, please restart the process.")
            return

        language_code = state_data['language_code']
        phone_number = message.contact.phone_number
        first_name = state_data['first_name']
        last_name = state_data['last_name']
        telegram_id = state_data['telegram_id']

        # Send the main menu based on the user's language preference
        await send_main_menu(message, language_code)

        # Perform database insertion
        insert_user_query(first_name=first_name, last_name=last_name, telegram_id=telegram_id,
                                language_code=language_code, phone_number=phone_number)

        # Delete the pending user entry
        delete_pending_user_by_telegram_id_query(telegram_id=message.from_user.id)

        # Clear the state
        await state.clear()

    except Exception as e:
        await message.answer(f"An error occurred during registration: {e}")

@router.callback_query(RegisterState.language_code)
async def register_language(callback: CallbackQuery, state: FSMContext):
    try:
        last_name = callback.from_user.last_name if callback.from_user.last_name else ''
        await callback.message.delete()

        # Send the appropriate message and keyboard for the selected language
        if callback.data == 'uz':
            await send_protected_message(callback.message, "Raqamingizni Kiriting...", reply_markup=share_number_uz)
        elif callback.data == 'ru':
            await send_protected_message(callback.message, "Введите свой номер...", reply_markup=share_number_rus)
        else:
            await send_protected_message(callback.message, "Enter your number...", reply_markup=share_number_eng)

        # Update the FSM state with user data
        await state.update_data(language_code=callback.data,
                                first_name=callback.from_user.first_name,
                                last_name=last_name,
                                telegram_id=callback.from_user.id)

        # Move to the phone number collection state
        await state.set_state(RegisterState.phone_number)

    except Exception as e:
        await callback.message.answer(f"An error occurred: {e}")
