from aiogram.types import Message, InputFile
from queries.for_users import get_user_by_telegram_id_query


async def send_protected_message(message: Message, content = None,
                                 photo = None, document = None,
                                 reply_markup=None, user_id=None, with_input=None,
                                 media_group: list=None):
    user_id = user_id if user_id else message.from_user.id
    protect = True
    is_super = get_user_by_telegram_id_query(user_id)
    if is_super['is_super']:
        protect = False

    if photo:
        if with_input:
            photo = InputFile(photo)
        await message.answer_photo(photo=photo, caption=content, protect_content=protect,
                                   reply_markup=reply_markup)
    elif document:
        if with_input:
            document = InputFile(document)
        await message.answer_document(document=document, caption=content, protect_content=protect,
                                      reply_markup=reply_markup)

    elif media_group and content:
        await message.answer_media_group(media=media_group, protect_content=protect)
        await message.answer(content, protect_content=protect, reply_markup=reply_markup)

    elif media_group:
        await message.answer_media_group(media=media_group, protect_content=protect,
                                         reply_markup=reply_markup)
    elif content:
        await message.answer(content, protect_content=protect, reply_markup=reply_markup)