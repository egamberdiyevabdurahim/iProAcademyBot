import re
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from buttons.for_auth import share_number_uz, choose_language_uz, \
    share_number_eng, share_number_rus, choose_language_ru, choose_language_en
from buttons.for_user import profiles_menu_en, profiles_menu_ru
from queries.for_balance import get_active_balance_by_user_id_query
from queries.for_users import get_user_by_telegram_id_query, update_user_query
from states.user_states import EditPhoneNumberState, EditLanguageState
from user.user.user_handlers import profile_go
from utils.activity_maker import activity_maker
from utils.addititons import PATTERN
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_registered_message, is_active, not_active_message

user_setting_router = Router()


@user_setting_router.message(
    F.text.in_({"Edit Phone Number", "Изменить Номер Телефона", "Telefon Raqamini O'zgartirish"}))
async def edit_phone_number(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            language = user_data.get('language')

            if language == "uz":
                await send_protected_message(message, f"Hozirgi Raqam: +{user_data['phone_number']}")
                await send_protected_message(message, "Yangi Telefon Raqamini Kiriting...", reply_markup=share_number_uz)
            elif language == "ru":
                await send_protected_message(message, f"Текущий номер: +{user_data['phone_number']}")
                await send_protected_message(message, "Введите новый номер телефона...", reply_markup=share_number_rus)
            else:
                await send_protected_message(message, f"Your current phone number: +{user_data['phone_number']}")
                await send_protected_message(message, "Enter new phone number...", reply_markup=share_number_eng)

            await state.set_state(EditPhoneNumberState.new_phone_number)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_setting_router.message(EditPhoneNumberState.new_phone_number)
async def new_phone_number(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            language = user_data.get('language_code')

            # Check if contact is shared in the message
            if message.contact:
                phone_number = message.contact.phone_number

                if re.match(PATTERN, phone_number):
                    await state.update_data(new_phone_number=phone_number)

                    if language == "uz":
                        await send_protected_message(message, f"Telefon Raqam O'zgartirildi: +{phone_number}")
                    elif language == "ru":
                        await send_protected_message(message, f"Новый номер телефона изменен: +{phone_number}")
                    else:
                        await send_protected_message(message, f"Your new phone number is: +{phone_number}")
                else:
                    if language == "uz":
                        await send_protected_message(message, "Nomer formati xato!")
                    elif language == "ru":
                        await send_protected_message(message, "Номер телефона неверный!")
                    else:
                        await send_protected_message(message, "Invalid phone number!")

                    await state.clear()
                    return await profile_go(message)

            elif message.text:
                phone_number = message.text
                if re.match(PATTERN, phone_number):
                    if phone_number[0] == '+':
                        phone_number = phone_number[1:]

                    await state.update_data(new_phone_number=phone_number)
                    if language == "uz":
                        await send_protected_message(message, f"Telefon Raqam O'zgartirildi: +{phone_number}")
                    elif language == "ru":
                        await send_protected_message(message, f"Новый номер телефона изменен: +{phone_number}")
                    else:
                        await send_protected_message(message, f"Your new phone number is: +{phone_number}")

                else:
                    if language == "uz":
                        await send_protected_message(message, "Nomer formati xato!")
                    elif language == "ru":
                        await send_protected_message(message, "Номер телефона неверный!")
                    else:
                        await send_protected_message(message, "Invalid phone number!")

                    await state.clear()
                    return await profile_go(message)

            # Update user data after valid input
            state_data = await state.get_data()

            update_user_query(user_id=user_data['id'],
                              phone_number=state_data['new_phone_number'],
                              language_code=user_data['language_code'],
                              first_name=user_data['first_name'],
                              last_name=user_data['last_name'],
                              telegram_id=user_data['telegram_id'])

            await state.clear()
            await profile_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_setting_router.message(F.text.in_({"Change Language", "Изменить Язык", "Tilni O'zgartirish"}))
async def change_language(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            language = user_data.get('language_code')

            if language == 'uz':
                await send_protected_message(message, "Yangi Til tanlang...", reply_markup=choose_language_uz)
            elif language == 'ru':
                await send_protected_message(message, "Выберите новый язык...", reply_markup=choose_language_ru)
            else:
                await send_protected_message(message, "Choose new language...", reply_markup=choose_language_en)

            # Store necessary data in FSM
            await state.update_data(user_id=user_data['id'],
                                    phone_number=user_data['phone_number'],
                                    first_name=user_data['first_name'],
                                    last_name=user_data['last_name'],
                                    telegram_id=user_data['telegram_id'])
            await state.set_state(EditLanguageState.language_code)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_setting_router.callback_query(EditLanguageState.language_code)
async def new_language(callback: CallbackQuery, state: FSMContext):
    if is_user_registered(callback.from_user.id):
        if await is_active(callback.message, user_id=callback.from_user.id):
            # Retrieve stored data from FSM
            data = await state.get_data()
            await callback.answer()

            # Change the language based on callback data
            if callback.data == "uz":
                await send_protected_message(callback.message, "Til O'zgartirildi: Uzbek", user_id=callback.from_user.id)
            elif callback.data == "ru":
                await send_protected_message(callback.message, "Язык изменен: Русский", user_id=callback.from_user.id)
            else:
                await send_protected_message(callback.message, "Language changed: English", user_id=callback.from_user.id)

            # Update the user's language in the database
            update_user_query(user_id=data['user_id'],
                              phone_number=data['phone_number'],
                              language_code=callback.data,
                              first_name=data['first_name'],
                              last_name=data['last_name'],
                              telegram_id=data['telegram_id'])

            # Clear the FSM state
            await state.clear()
            await callback.message.delete()

            # Go back to profile menu
            await profile_go(callback.message, user_id=callback.from_user.id)

        else:
            await not_active_message(callback.message)

    else:
        await not_registered_message(callback.message)


@user_setting_router.message(F.text.in_({"Show My Data", "Показать Мои Данные", "Ma'lumotlarimni ko'rish"}))
async def show_my_data(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            language = user_data.get('language_code')
            is_go = True
            is_end = False
            if user_data['is_super'] is False:
                user_balance = get_active_balance_by_user_id_query(user_id=user_data['id'])
                left = (user_balance['ends_at'] - datetime.date(datetime.now())).days

                if left == 0:
                    is_end = True

            else:
                is_go = False
                left = ''

            if language == "uz":
                if is_go:
                    if is_end:
                        left = "Bugun So'ngi Kun!"

                    else:
                        left = f"{left}-kun Qoldi"

                await send_protected_message(message, f"Hisob tafsilotlari\n"
                                                      f"👤 Foydalanuvchi nomi: @{message.from_user.username}\n"
                                                      f"🙋‍♂️ Ism: {user_data['first_name']} {user_data['last_name']}\n"
                                                      f"📞 Telefon: +{user_data['phone_number']}\n"
                                                      f"🆔 Telegram ID: {user_data['telegram_id']}\n"
                                                      f"🇺🇿 Muloqot tili: O'zbek Tili\n"
                                                      f"💰 Balans: {left}")

            elif language == "ru":
                if is_go:
                    if is_end:
                        left = "Сегодня последний день!"

                    else:
                        left = f"{left}-дней осталось"

                await send_protected_message(message, f"Данные счета\n"
                                                      f"👤 Имя пользователя: @{message.from_user.username}\n"
                                                      f"🙋‍♂️ Имя: {user_data['first_name']} {user_data['last_name']}\n"
                                                      f"📞 Телефон: +{user_data['phone_number']}\n"
                                                      f"🆔 Телеграм ID: {user_data['telegram_id']}\n"
                                                      f"🇷🇺 Язык общения: Русский\n"
                                                      f"💰 Баланс: {left}")

            else:
                if is_go:
                    if is_end:
                        left = "Today is the last day!"

                    else:
                        left = f"{left}-days to end"

                await send_protected_message(message, f"Account Details\n"
                                                      f"👤 Username: @{message.from_user.username}\n"
                                                      f"🙋‍♂️ Full Name: {user_data['first_name']} {user_data['last_name']}\n"
                                                      f"📞 Phone: +{user_data['phone_number']}\n"
                                                      f"🆔 Telegram iD: {user_data['telegram_id']}\n"
                                                      f"🇺🇸 Language: English\n"
                                                      f"💰 Balance: {left}")

            await profile_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_setting_router.message(F.text.in_({"💵Balance", "💵Баланс", "💵Balans"}))
async def balance_handler(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            language = user_data.get('language_code')

            if user_data['is_super'] is True:
                await send_protected_message(message, "You Are Super Admin!")
                return

            user_balance = get_active_balance_by_user_id_query(user_id=user_data['id'])
            if user_balance is None:
                await send_protected_message(message, "You have no balance!")
                return

            left = user_balance['ends_at'] - datetime.date(datetime.now())

            is_end = False
            if left == 0:
                is_end = True

            if language == "uz":
                if is_end:
                    await send_protected_message(message, f"Bugun So'ngi Kun!\n"
                                                      f"Boshlangan vaqti: {user_balance['starts_at']}\n"
                                                      f"Tugash vaqti: {user_balance['ends_at']}")
                else:
                    await send_protected_message(message, f"{left.days} Kun Qoldi\n"
                                                          f"Boshlangan vaqti: {user_balance['starts_at']}\n"
                                                          f"Tugash vaqti: {user_balance['ends_at']}")

            elif language == "ru":
                if is_end:
                    await send_protected_message(message, f"Сегодня осталось последний день!\n"
                                                      f"Начало действия: {user_balance['starts_at']}\n"
                                                      f"Конец действия: {user_balance['ends_at']}")

                else:
                    await send_protected_message(message, f"{left.days} дней осталось\n"
                                                          f"Дата начала активности: {user_balance['starts_at']}\n"
                                                          f"Дата конца активности: {user_balance['ends_at']}")

            else:
                if is_end:
                    await send_protected_message(message, f"Today is the last day!\n"
                                                      f"Started date: {user_balance['starts_at']}\n"
                                                      f"Ending date: {user_balance['ends_at']}")
                else:
                    await send_protected_message(message, f"{left.days} days to end\n"
                                                          f"Started date: {user_balance['starts_at']}\n"
                                                          f"Ending date: {user_balance['ends_at']}")

            await profile_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)