from aiogram.types import Message

from queries.for_users import get_user_by_telegram_id_query


async def send_protected_message(message: Message, content: str = None,
                                 photo: str = None, document = None,
                                 reply_markup=None, user_id=None):

    user_id = user_id if user_id else message.from_user.id
    protect = True
    is_super = get_user_by_telegram_id_query(user_id)
    if is_super['is_super'] is True:
        protect = False
    if content:
        await message.answer(content, protect_content=protect, reply_markup=reply_markup)
    elif photo:
        await message.answer_photo(photo=photo, protect_content=protect, reply_markup=reply_markup)
    elif document:
        await message.answer_document(document=document, protect_content=protect, reply_markup=reply_markup)
