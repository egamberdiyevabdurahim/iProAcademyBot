from queries import for_users


def is_user_registered(telegram_id: int) -> bool:
    """
    Checks if a user with the given Telegram ID is registered in the database.

    Args:
    telegram_id (str): The user's Telegram ID.

    Returns:
    bool: True if the user is registered, False otherwise.
    """
    data = for_users.get_user_by_telegram_id_query(telegram_id)
    return data is not None


def get_user_data(telegram_id):
    """
    Retrieves user data from the database based on their Telegram ID.

    Args:
    telegram_id (str): The user's Telegram ID.

    Returns:
    DictRow: The user's data from the database.
    """
    return for_users.get_user_by_telegram_id_query(telegram_id)
