from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_aop_panic_table_query() -> None:
    """
    Creates a table for storing AOP panic notifications.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS aop_panic (
        id BIGSERIAL PRIMARY KEY,
        name_uz TEXT NOT NULL,
        name_ru TEXT NOT NULL,
        name_en TEXT NOT NULL,
        code VARCHAR(64) NOT NULL,
        user_id BIGINT REFERENCES users(id),
        status BOOLEAN DEFAULT TRUE,    
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_aop_panic_query(name_uz: str, name_ru: str, name_en: str, code: str, user_id: int) -> None:
    """
    Inserts a new AOP panic notification into the aop_panic table.
    """
    query = """
    INSERT INTO aop_panic (name_uz, name_ru, name_en, code, user_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (name_uz, name_ru, name_en, code, user_id))
    return None


def update_aop_panic_query(id_of: int, new_name_uz: str, new_name_ru: str, new_name_en: str, code: str) -> None:
    """
    Updates an AOP panic notification.
    """
    query = """
    UPDATE aop_panic
    SET name_uz=%s, name_ru=%s, name_en=%s, code=%s, updated_at=%s
    WHERE id=%s
    """
    execute_query(query, (new_name_uz, new_name_ru, new_name_en, code, datetime.now(), id_of))
    return None


def delete_aop_panic_query(id_of: int) -> None:
    """
    Deletes an AOP panic notification from the aop_panic table.
    """
    query = "UPDATE aop_panic SET status=%s WHERE id=%s"
    execute_query(query, (False, id_of))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_aop_panic_by_id_query(id_of: int) -> DictRow:
    """
    Retrieves an AOP panic notification by its ID.
    """
    query = "SELECT * FROM aop_panic WHERE id=%s AND status=%s"
    return execute_query(query, (id_of, True), fetch="one")


def get_aop_panic_by_code_query(code: str) -> DictRow:
    """
    Retrieves an AOP panic notification by its code.
    """
    query = "SELECT * FROM aop_panic WHERE code=%s AND status=%s"
    return execute_query(query, (code, True), fetch="one")


def get_aop_panic_by_name_uz_query(name_uz: str) -> DictRow:
    """
    Retrieves an AOP panic notification by its name_uz.
    """
    query = "SELECT * FROM aop_panic WHERE name_uz=%s AND status=%s"
    return execute_query(query, (name_uz, True), fetch="one")


def get_aop_panic_by_name_ru_query(name_ru: str) -> DictRow:
    """
    Retrieves an AOP panic notification by its name_ru.
    """
    query = "SELECT * FROM aop_panic WHERE name_ru=%s AND status=%s"
    return execute_query(query, (name_ru, True), fetch="one")


def get_aop_panic_by_name_en_query(name_en: str) -> DictRow:
    """
    Retrieves an AOP panic notification by its name_en.
    """
    query = "SELECT * FROM aop_panic WHERE name_en=%s AND status=%s"
    return execute_query(query, (name_en, True), fetch="one")


def get_all_aop_panics_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all AOP panic notifications by their user ID.
    """
    query = "SELECT * FROM aop_panic WHERE user_id=%s AND status=%s"
    return execute_query(query, (user_id, True), fetch="all")


def get_all_aop_panics_query() -> list:
    """
    Retrieves all AOP panic notifications.
    """
    query = "SELECT * FROM aop_panic WHERE status=%s"
    return execute_query(query, (True,), fetch="all")
