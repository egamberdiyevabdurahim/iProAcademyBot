from aiogram.types import Message, CallbackQuery

from queries.for_balance import get_active_balance_by_user_id_query
from queries.for_users import get_user_by_telegram_id_query
from utils.addititons import ADMIN_LINK


async def not_registered_message_uz(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - siz Academiya uquvchisi emassiz botdan foydalanish uchun\n{ADMIN_LINK} "
        f"ga murojat qiling!")


async def not_registered_message_ru(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - вы не являетесь студентом Академии iPro, пожалуйста, "
        f"свяжитесь с {ADMIN_LINK} для использования бота!")


async def not_registered_message_en(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - You are not an Academy student, please contact {ADMIN_LINK} to use the bot!")


async def not_registered_message(message: Message):
    if message.from_user.language_code == 'uz':
        await not_registered_message_uz(message)
    elif message.from_user.language_code == 'ru':
        await not_registered_message_ru(message)
    else:
        await not_registered_message_en(message)


async def not_admin_message_ru(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - Вы не являетесь администратором, пожалуйста, свяжитесь с {ADMIN_LINK} "
        f"для использования бота как администратор!")


async def not_admin_message_uz(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - Siz admin emassiz, botni admin sifatida ishlatish uchun {ADMIN_LINK} - bilan "
        f"bog'laning!")


async def not_admin_message_en(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - You are not an administrator, please contact {ADMIN_LINK} to use the bot as an admin!")


async def not_admin_message(message: Message):
    language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
    if language == 'uz':
        await not_admin_message_uz(message)
    elif language == 'ru':
        await not_admin_message_ru(message)
    else:
        await not_admin_message_en(message)


async def not_active_message_uz(message: Message):
    await message.answer(
        f"Hisobingizda yetarli Mablağ mavjud emas iltimos {ADMIN_LINK} ga murojat qiling")


async def not_active_message_ru(message: Message):
    await message.answer(
        f"На вашем счету недостаточно средств, обратитесь к {ADMIN_LINK}")


async def not_active_message_en(message: Message):
    await message.answer(
        f"Your account does not have enough funds, please contact the {ADMIN_LINK}")


async def not_active_message(message: Message):
    language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
    if language == 'uz':
        await not_active_message_uz(message)
    elif language == 'ru':
        await not_active_message_ru(message)
    else:
        await not_active_message_en(message)


async def not_super_admin_message_uz(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - Siz Bot Egasi Emassiz!")


async def not_super_admin_message_ru(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - Вы не являетесь суперадминистратором!")


async def not_super_admin_message_en(message: Message):
    await message.answer(
        f"{message.from_user.first_name} - You are not a super administrator!")


async def not_super_admin_message(message: Message):
    language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
    if language == 'uz':
        await not_super_admin_message_uz(message)
    elif language == 'ru':
        await not_super_admin_message_ru(message)
    else:
        await not_super_admin_message_en(message)


async def is_active(message: Message):
    user_data = get_user_by_telegram_id_query(message.from_user.id)
    if user_data['is_super'] is False:
        balance_data = get_active_balance_by_user_id_query(user_data['id'])
        if balance_data is None:
            return False
    return True


async def is_active_for_callback(callback: CallbackQuery):
    user_data = get_user_by_telegram_id_query(callback.from_user.id)
    if user_data['is_super'] is False:
        balance_data = get_active_balance_by_user_id_query(user_data['id'])
        if balance_data is None:
            return False
    return True
