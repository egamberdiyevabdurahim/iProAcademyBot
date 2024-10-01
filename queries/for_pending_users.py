from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_pending_user_table_query() -> None:
    """
    Creates a table for storing pending users.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS pending_users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status BOOLEAN DEFAULT TRUE
    )
    """)
    return None


def insert_pending_user_query(telegram_id: int) -> None:
    query = """
    INSERT INTO pending_users (telegram_id)
    VALUES (%s)
    """
    execute_query(query, (telegram_id,))
    return None


def delete_pending_user_by_id_query(id_of: int) -> None:
    query = """
    UPDATE pending_users
    SET status=%s
    WHERE id=%s AND status=%s"""
    execute_query(query, (False, id_of, True))
    return None


def delete_pending_user_by_telegram_id_query(telegram_id: int) -> None:
    query = """
    UPDATE pending_users
    SET status=%s
    WHERE telegram_id=%s AND status=%s"""
    execute_query(query, (False, telegram_id, True))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_pending_user_by_telegram_id_query(telegram_id: int) -> DictRow:
    query = """
    SELECT * FROM pending_users
    WHERE telegram_id = %s AND status = %s"""
    return execute_query(query, (telegram_id, True), fetch="one")


def get_pending_user_by_id_query(id_of: int) -> DictRow:
    query = """
    SELECT * FROM pending_users
    WHERE id = %s AND status = %s"""
    return execute_query(query, (id_of, True), fetch="one")


def get_all_pending_users_query() -> list:
    query = """
    SELECT * FROM pending_users
    WHERE status = %s"""
    return execute_query(query, (True,), fetch="all")
