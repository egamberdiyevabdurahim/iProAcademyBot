from aiogram.types import Message, CallbackQuery

from queries.for_activity import insert_activity_query
from queries.for_users import add_used_by_id_query, get_user_by_telegram_id_query


async def activity_maker(message: Message, user_id=None):
    user_id = user_id if user_id else message.from_user.id
    user_id_data = get_user_by_telegram_id_query(user_id)['id']
    insert_activity_query(text=message.text, user_id=user_id_data, with_id=message.message_id)
    add_used_by_id_query(user_id_data)
    return None


async def activity_maker_for_callback(callback: CallbackQuery):
    user_id_data = get_user_by_telegram_id_query(callback.from_user.id)['id']
    insert_activity_query(text=callback.message.text, user_id=user_id_data)
    add_used_by_id_query(user_id_data)
    return None
