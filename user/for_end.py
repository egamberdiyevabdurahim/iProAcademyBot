from aiogram import Router, F, Bot
from aiogram.types import Message, InputMediaPhoto, InputMedia, FSInputFile, InputFile

from database_config.config import TOKEN
from queries.for_users import get_user_by_telegram_id_query
from utils.activity_maker import activity_maker
from utils.proteceds import send_protected_message

end_router = Router()
bot = Bot(token=TOKEN)


@end_router.message(F.text)
async def end_go(message: Message):
    await activity_maker(message)

    user_language = get_user_by_telegram_id_query(message.from_user.id)
    if user_language['language_code'] == "uz":
        await send_protected_message(message, "Xato Buyruq!")

    elif user_language['language_code'] == "ru":
        await send_protected_message(message, "Ошибочный запрос!")

    else:
        await send_protected_message(message, "Wrong request!")
