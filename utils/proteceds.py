from aiogram.types import Message


async def send_protected_message(message: Message, content: str = None, photo: str = None, document = None, reply_markup=None):
    if content:
        await message.answer(content, protect_content=True, reply_markup=reply_markup)
    elif photo:
        await message.answer_photo(photo=photo, protect_content=True, reply_markup=reply_markup)
    elif document:
        await message.answer_document(document=document, protect_content=True, reply_markup=reply_markup)
