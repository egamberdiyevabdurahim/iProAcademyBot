from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaDocument

from database_config.config import TOKEN
from queries.for_users import get_all_users_query, get_user_by_telegram_id_query
from states.super_state import SendMessageState
from utils.activity_maker import activity_maker
from utils.for_auth import is_user_registered
from utils.validator import is_active, not_super_admin_message, not_registered_message, not_active_message

message_sender_super_router = Router()
bot = Bot(token=TOKEN)


@message_sender_super_router.message(F.text == '/send')
async def send_chat(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            user_data = get_user_by_telegram_id_query(message.from_user.id)
            if user_data['is_super'] is False:
                await not_super_admin_message(message)
                return

            await message.answer("Send Message Fully:")
            await state.set_state(SendMessageState.send)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@message_sender_super_router.message(SendMessageState.send)
async def send_message(message: Message, state: FSMContext):
    users = get_all_users_query()

    for user in users:
        try:
            media_group = []

            # Collect highest quality photos
            if message.photo:
                for photo in message.photo:
                    media_group.append(InputMediaPhoto(media=photo.file_id))

            # Collect videos, if any
            if message.video:
                media_group.append(InputMediaVideo(media=message.video.file_id))

            # Collect documents, if any
            if message.document:
                media_group.append(InputMediaDocument(media=message.document.file_id))

            # Send the media group if we have collected any media
            if media_group:
                await bot.send_media_group(chat_id=user['telegram_id'], media=media_group)
            else:
                # If no media, send text message
                await bot.send_message(chat_id=user['telegram_id'], text=message.text)

        except Exception as e:
            await message.answer(f"Failed to send to {user['telegram_id']}: {str(e)}")

    await message.answer("Message sent to users successfully!")
    await state.clear()
