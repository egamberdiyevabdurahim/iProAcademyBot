from datetime import datetime

from aiogram import Bot

from buttons.for_user import main_menu_first_uz, main_menu_first_en, main_menu_first_ru
from database_config.config import TOKEN
from queries.for_activity import get_last_activity_by_user_id_query, get_yesterdays_first_activity_by_user_id_query
from queries.for_balance import get_all_active_balance_query, deactivate_balance_by_id_query, \
    get_all_future_active_balance_query, activate_balance_by_id_query
from queries.for_users import get_user_by_id_query, get_all_users_query
from utils.addititons import ADMIN_LINK

bot = Bot(token=TOKEN)


async def disabled_balance_sender(user_id):
    user_data = get_user_by_id_query(user_id)
    if user_data:
        language = user_data['language_code']
        text = None
        if language == 'uz':
            text = (f"{user_data['first_name']} {user_data['last_name']}\nSizning Hisobingiz o'chirildi\n"
                    f"{ADMIN_LINK} bilan bog'lanib hisobingizni yoqtiring!")

        elif language == 'ru':
            text = (f"{user_data['first_name']} {user_data['last_name']}\nВаш аккаунт был отключен\n"
                    f"Свяжитесь с {ADMIN_LINK}, чтобы активировать ваш аккаунт!")

        elif language == 'en':
            text = (f"{user_data['first_name']} {user_data['last_name']}\nYour account has been disabled\n"
                    f"Contact {ADMIN_LINK} to activate your account!")

        await bot.send_message(chat_id=user_data['telegram_id'], text=text, protect_content=True)


async def balance_calculater():
    balances_data = get_all_active_balance_query()  # assuming you have an async version
    for balance in balances_data:
        if balance['ends_at'] < datetime.now().date():
            deactivate_balance_by_id_query(balance['id'])
            await disabled_balance_sender(balance['user_id'])


async def end_date_sender(balance, user, days):
    language = user['language_code']
    text = None
    code = None
    if language == 'uz':
        code = f"Va <code>{user['telegram_id']}</code> - shuni adminga berishni unitmang!"
        if days == 10:
            text=(f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz o'chishiga 10 kun qoldi\n"
                  f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

        elif days == 5:
            text=(f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz o'chishiga 5 kun qoldi\n"
                  f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

        elif days == 3:
            text = (f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz o'chishiga 3 kun qoldi\n"
                    f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

        elif days == 2:
            text = (f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz o'chishiga 2 kun qoldi\n"
                    f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

        elif days == 1:
            text = (f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz o'chishiga 1 kun qoldi\n"
                    f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

        elif days == 0:
            text = (f"{user['first_name']} {user['last_name']}\nSiznig Hisobingiz Bugun O'chadi\n"
                  f"{ADMIN_LINK} bilan bog'lanib hisobingizni uzaytirib oling")

    elif language == 'en':
        code = f"And don't forget to give this to the admin - <code>{user['telegram_id']}</code>!"
        if days == 10:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled in 10 days\n"
                    f"Contact {ADMIN_LINK} to extend your account")

        elif days == 5:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled in 5 days\n"
                    f"Contact {ADMIN_LINK} to extend your account")

        elif days == 3:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled in 3 days\n"
                    f"Contact {ADMIN_LINK} to extend your account")

        elif days == 2:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled in 2 days\n"
                    f"Contact {ADMIN_LINK} to extend your account")

        elif days == 1:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled in 1 day\n"
                    f"Contact {ADMIN_LINK} to extend your account")

        elif days == 0:
            text = (f"{user['first_name']} {user['last_name']}\nYour account will be disabled today\n"
                    f"Contact {ADMIN_LINK} to extend your account")

    elif language == 'ru':
        code = f"И не забудьте передать это администратору - <code>{user['telegram_id']}</code>!"
        if days == 10:
            text = (f"{user['first_name']} {user['last_name']}\nДо отключения вашего аккаунта осталось 10 дней\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

        elif days == 5:
            text = (f"{user['first_name']} {user['last_name']}\nДо отключения вашего аккаунта осталось 5 дней\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

        elif days == 3:
            text = (f"{user['first_name']} {user['last_name']}\nДо отключения вашего аккаунта осталось 3 дня\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

        elif days == 2:
            text = (f"{user['first_name']} {user['last_name']}\nДо отключения вашего аккаунта осталось 2 дня\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

        elif days == 1:
            text = (f"{user['first_name']} {user['last_name']}\nДо отключения вашего аккаунта остался 1 день\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

        elif days == 0:
            text = (f"{user['first_name']} {user['last_name']}\nВаш аккаунт будет удалён сегодня\n"
                    f"Свяжитесь с {ADMIN_LINK} для продления вашего аккаунта")

    await bot.send_message(chat_id=user['telegram_id'], text=text, protect_content=True)
    await bot.send_message(chat_id=user['telegram_id'], text=code, protect_content=False, parse_mode="HTML")


async def end_date_checker():
    balances = get_all_active_balance_query()
    for balance in balances:
        user_data = get_user_by_id_query(balance['user_id'])
        if (balance['ends_at'] - datetime.date(datetime.now())).days == 10:
            await end_date_sender(balance, user_data, 10)

        elif (balance['ends_at'] - datetime.date(datetime.now())).days == 5:
            await end_date_sender(balance, user_data, 5)

        elif (balance['ends_at'] - datetime.date(datetime.now())).days == 3:
            await end_date_sender(balance, user_data, 3)

        elif (balance['ends_at'] - datetime.date(datetime.now())).days == 2:
            await end_date_sender(balance, user_data, 2)

        elif (balance['ends_at'] - datetime.date(datetime.now())).days == 1:
            await end_date_sender(balance, user_data, 1)

        elif (balance['ends_at'] - datetime.date(datetime.now())).days == 0:
            await end_date_sender(balance, user_data, 0)


async def balance_activator():
    balances = get_all_future_active_balance_query()
    if len(balances) == 0:
        return

    for balance in balances:
        activate_balance_by_id_query(balance['id'])


async def message_deleter():
    users_data = get_all_users_query()
    for user_data in users_data:
        user_id = user_data['id']
        language_code = user_data['language_code']
        telegram_id = user_data['telegram_id']

        # Get the first message data (handle None case)
        first_message_data = get_yesterdays_first_activity_by_user_id_query(user_id=user_id)
        first_message_id = int(first_message_data['with_id']) if first_message_data else 1

        # Get the last message data (handle None case)
        last_message_data = get_last_activity_by_user_id_query(user_id)
        last_message_id = int(last_message_data['with_id']) if last_message_data else 1

        # Define the message range (with a safety buffer of 50 messages before and after)
        message_range = range(first_message_id - 50, last_message_id + 50)

        # Delete messages one by one (since batch deletion is not supported)
        for message_id in message_range:
            try:
                await bot.delete_message(chat_id=telegram_id, message_id=message_id)

            except Exception as e:
                print(e)

        # Send a welcome message based on language
        try:
            if language_code == 'uz':
                await bot.send_message(chat_id=telegram_id,
                                       text=f"Assalomu Aleykum {user_data['first_name']}\n"
                                            f"iPro Academy-ga Xush Kelibsiz!",
                                       reply_markup=main_menu_first_uz,
                                       protect_content=True)
            elif language_code == 'ru':
                await bot.send_message(chat_id=telegram_id,
                                       text=f"Добро Пожаловать в iPro Academy {user_data['first_name']}!",
                                       reply_markup=main_menu_first_ru,
                                       protect_content=True)
            else:
                await bot.send_message(chat_id=telegram_id,
                                       text=f"Welcome to iPro Academy {user_data['first_name']}!",
                                       reply_markup=main_menu_first_en,
                                       protect_content=True)

        except Exception as e:
            print(e)

