from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_users_table_query() -> None:
    """
    Creates a table for storing users.
    """
    execute_query("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")
    execute_query("""
    CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    code uuid default uuid_generate_v4(),
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64),
    telegram_id BIGINT NOT NULL,
    language_code VARCHAR(64),
    phone_number VARCHAR(64),
    is_admin BOOLEAN DEFAULT FALSE,
    is_super BOOLEAN DEFAULT FALSE,
    used BIGINT DEFAULT 0,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_user_query(first_name: str, telegram_id: int, language_code: str, phone_number: str, last_name: str=None) -> None:
    query = """
    INSERT INTO users (first_name, last_name, telegram_id, language_code, phone_number)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (first_name, last_name, telegram_id, language_code, phone_number))
    return None


def add_admin_by_id_query(user_id) -> None:
    query = "UPDATE users SET is_admin=TRUE WHERE id=%s"
    execute_query(query, (user_id,))
    return None


def add_used_by_id_query(user_id: int) -> None:
    query = "UPDATE users SET used=used+1 WHERE id=%s"
    execute_query(query, (user_id,))
    return None


def update_user_query(user_id: int, first_name: str, telegram_id: int, language_code: str, phone_number: str, last_name: str) -> None:
    query = ("""
    UPDATE users
    SET first_name=%s, last_name=%s, telegram_id=%s, language_code=%s, phone_number=%s
    WHERE id=%s AND status=%s""")
    execute_query(query, (first_name, last_name, telegram_id, language_code, phone_number, user_id, True))
    return None


def delete_user_query(user_id: int) -> None:
    query = "UPDATE users SET status=%s WHERE id=%s"
    execute_query(query, (False, user_id))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_user_by_id_query(user_id) -> DictRow:
    query = "SELECT * FROM users WHERE id = %s AND status = %s"
    return execute_query(query, (user_id, True), fetch="one")


def get_user_by_telegram_id_query(telegram_id) -> DictRow:
    query = "SELECT * FROM users WHERE telegram_id = %s AND status = %s"
    return execute_query(query, (telegram_id, True), fetch="one")


def get_all_admins_query() -> list:
    query = "SELECT * FROM users WHERE is_admin = %s AND status = %s"
    return execute_query(query, (True, True), fetch="all")


def get_user_by_phone_number_query(phone_number: str) -> DictRow:
    query = "SELECT * FROM users WHERE phone_number = %s AND status = %s"
    return execute_query(query, (str(phone_number), True), fetch="one")


def get_user_by_code_query(code: str) -> DictRow:
    query = "SELECT * FROM users WHERE code = %s AND status = %s"
    return execute_query(query, (code, True), fetch="one")


def get_admin_users_query() -> list:
    query = "SELECT * FROM users WHERE is_admin = %s AND status = %s"
    return execute_query(query, (True, True), fetch="all")


def get_all_users_query() -> list:
    query = "SELECT * FROM users WHERE status = %s ORDER BY id DESC"
    return execute_query(query, (True,), fetch="all")


def get_inactive_users_query() -> list:
    query = """
    SELECT * FROM users u
    LEFT JOIN balance b ON u.id = b.user_id
    WHERE u.status = %s AND (b.is_active = %s OR b IS NULL)
    ORDER BY u.id DESC
    """
    return execute_query(query, (True, False), fetch="all")
