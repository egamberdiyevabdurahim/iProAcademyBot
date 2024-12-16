from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from buttons.for_admin import admin_main_menu
from buttons.for_super_admin import super_admin_main_menu
from buttons.for_user import after_apple_menu, panic_array_menu, userspace_menu, aop_panic_menu, \
    alphabets_menu, i2c_category_menu, profiles_menu_uz, profiles_menu_ru, profiles_menu_en, apple_menu_en, \
    swap_menu, itunes_menu, tools_menu_en, tools_menu_uz, tools_menu_ru, imei_generator_menu_en, \
    imei_generator_menu_ru, imei_generator_menu_uz, apple_menu_uz, apple_menu_ru

from queries.for_users import get_user_by_telegram_id_query

from states.user_states import PanicState, UserSpaceState, AOPPanicState, AlphabetsState, I2CState, SwapState, \
    ITunesState

from utils.activity_maker import activity_maker

from utils.addititons import ALPHABETS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import not_admin_message, not_registered_message, is_active, not_active_message

user_router = Router()


@user_router.message(F.text == "Apple")
async def apple_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if language == 'en':
                await send_protected_message(message, "Apple", reply_markup=apple_menu_en)

            elif language == 'uz':
                await send_protected_message(message, "Apple", reply_markup=apple_menu_uz)

            elif language == 'ru':
                await send_protected_message(message, "Apple", reply_markup=apple_menu_ru)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "PANIC")
async def panic_menu_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "Panic Menu", reply_markup=await after_apple_menu(language))

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "SWAP")
async def swap_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "Swap", reply_markup=await swap_menu(language))
            await state.set_state(SwapState.to_data)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "iTunes")
async def itunes_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "iTunes", reply_markup=await itunes_menu(language))
            await state.set_state(ITunesState.to_data)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "Android")
async def android_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await send_protected_message(message, "Coming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"⚙️Инструменты", "⚙️Tools", "⚙️Uskunalar"}))
async def tools_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if language == "uz":
                await send_protected_message(message, "⚙️Uskunalar", reply_markup=tools_menu_uz)

            elif language == "ru":
                await send_protected_message(message, "⚙️Инструменты", reply_markup=tools_menu_ru)

            elif language == "en":
                await send_protected_message(message, "⚙️Tools", reply_markup=tools_menu_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"⚙️IMEI Generator", "⚙️IMEI Генератор"}))
async def imei_generator_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if language == "uz":
                await send_protected_message(message, "Ushbu IMEI lar uzimei tizimida Talab etilmaydigan imei lar!", reply_markup=imei_generator_menu_uz)

            elif language == "ru":
                await send_protected_message(message, "Эти IMEI являются ненужными имейсами в системе uzimei!", reply_markup=imei_generator_menu_ru)

            elif language == "en":
                await send_protected_message(message, "These IMEI are Unnecessary IMEI in the uzimei system!", reply_markup=imei_generator_menu_en)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


# @user_router.message(F.text.in_({"⚙️IMEI Checker", "⚙️IMEI Tekshirish", "⚙️Проверка IMEI"}))
# async def imei_checker_go(message: Message, state: FSMContext):
#     if is_user_registered(message.from_user.id):
#         if await is_active(message):
#             await activity_maker(message)
#
#             language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
#             if language == "uz":
#                 await send_protected_message(message, "IMEI-ni Kiriting:")
#
#             elif language == "ru":
#                 await send_protected_message(message, "Введите IMEI:")
#
#             elif language == "en":
#                 await send_protected_message(message, "Enter IMEI:")
#
#             await state.set_state(ImeiCheckerState.imei)
#
#         else:
#             await not_active_message(message)
#
#     else:
#         await not_registered_message(message)
#

@user_router.message(F.text.in_({"⚙️Setting", "⚙️Настройки", "⚙️Sozlamalar"}))
async def profile_go(message: Message, user_id=None):
    if not user_id:
        user_id = message.from_user.id
    if is_user_registered(user_id):
        if await is_active(message, user_id=user_id):
            await activity_maker(message, user_id=user_id)

            user_language = get_user_by_telegram_id_query(user_id)['language_code']
            if user_language == "uz":
                await send_protected_message(message, "⚙️Sozlamalar", reply_markup=profiles_menu_uz, user_id=user_id)

            elif user_language == "ru":
                await send_protected_message(message, "⚙️Настройки", reply_markup=profiles_menu_ru, user_id=user_id)

            else:
                await send_protected_message(message, "⚙️Setting", reply_markup=profiles_menu_en, user_id=user_id)

        else:
            await not_active_message(message)
    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"🔙Back To Apple Menu", "🔙Вернуться к Apple меню", "🔙Apple menyuga qaytish", "🔙Apple menyusiga qaytish"}))
async def back_to_apple_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await panic_menu_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"🔙Back To Tool Menu", "🔙Вернуться в меню инструментов", "🔙Asboblar menyusiga qaytish"}))
async def back_to_apple_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await tools_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "🔙Back To Android Menu")
async def back_to_apple_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await android_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"🔙Back To Choosing Menu", "🔙Вернуться к выбору меню", "🔙Tanlash menyusiga qaytish"}))
async def back_to_apple_menu(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await apple_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text.in_({"🔙Back To Swap Menu", "🔙Вернуться к меню swap", "🔙Swap menyuga qaytish"}))
async def back_to_apple_menu(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await swap_go(message, state)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "SMC PANIC - ASSERTION")
async def panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if await panic_array_menu(language) is not None:
                await activity_maker(message)

                language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
                await send_protected_message(message, "SMC PANIC - ASSERTION", reply_markup=await panic_array_menu(language))
                await state.set_state(PanicState.to_array)

            else:
                await send_protected_message(message, "Coming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "Userspace watchdog timeout")
async def userspace_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "Userspace watchdog timeout", reply_markup=await userspace_menu(language))
            await state.set_state(UserSpaceState.to_data)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "i2c")
async def i2c_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "i2c", reply_markup=await i2c_category_menu(language))
            await state.set_state(I2CState.to_category)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "AOP PANIC")
async def aop_panic_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            await send_protected_message(message, "AOP PANIC", reply_markup=await aop_panic_menu(language))
            await state.set_state(AOPPanicState.to_data)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(F.text == "ADMIN")
async def admin_go(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_admin'] is False:
                await not_admin_message(message)
                return

            if user_data['is_super'] is True:
                await send_protected_message(message, "Super Admin", reply_markup=super_admin_main_menu)

            else:
                await send_protected_message(message, "Admin", reply_markup=admin_main_menu)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_router.message(lambda message: message.text and message.text.upper() in ALPHABETS)
async def alphabets_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            markup = await alphabets_menu(message.text, language)

            if markup is not None and isinstance(markup, ReplyKeyboardMarkup):
                await send_protected_message(message, f"Panics starting with letter ({message.text}):", reply_markup=markup)
                await state.set_state(AlphabetsState.to_data)
            else:
                await send_protected_message(message, "Coming Soon🔥")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
