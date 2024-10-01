from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_userspace_table_query() -> None:
    """
    Creates a table for storing user spaces.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS userspace (
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


def insert_userspace_query(name_uz: str, name_ru: str, name_en: str, code: str, user_id: int) -> None:
    """
    Inserts a new user space into the userspace table.
    """
    query = """
    INSERT INTO userspace (name_uz, name_ru, name_en, code, user_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (name_uz, name_ru, name_en, code, user_id))
    return None


def update_userspace_query(userspace_id: int, new_name_uz: str, new_name_ru: str, new_name_en: str, code: str) -> None:
    """
    Updates a user space.
    """
    query = ("""
    UPDATE userspace
    SET name_uz=%s, name_ru=%s, name_en=%s, code=%s, updated_at=%s, language_id=%s
    WHERE id=%s AND status=%s""")
    execute_query(query, (new_name_uz, new_name_ru, new_name_en, code, datetime.now(), userspace_id, True))
    return None


def delete_userspace_query(userspace_id: int) -> None:
    """
    Deletes a user space from the userspace table.
    """
    query = "UPDATE userspace SET status=%s WHERE id=%s"
    execute_query(query, (False, userspace_id))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_userspace_by_id_query(userspace_id: int) -> DictRow:
    """
    Retrieves a user space by its ID.
    """
    query = "SELECT * FROM userspace WHERE id=%s AND status=%s"
    return execute_query(query, (userspace_id, True), fetch="one")


def get_userspace_by_code_query(code: str) -> DictRow:
    """
    Retrieves a user space by its code.
    """
    query = "SELECT * FROM userspace WHERE code=%s AND status=%s"
    return execute_query(query, (code, True), fetch="one")


def get_userspace_by_name_uz_query(name_uz: str) -> DictRow:
    """
    Retrieves a user space by its name_uz.
    """
    query = "SELECT * FROM userspace WHERE name_uz=%s AND status=%s"
    return execute_query(query, (name_uz, True), fetch="one")


def get_userspace_by_name_ru_query(name_ru: str) -> DictRow:
    """
    Retrieves a user space by its name_ru.
    """
    query = "SELECT * FROM userspace WHERE name_ru=%s AND status=%s"
    return execute_query(query, (name_ru, True), fetch="one")


def get_userspace_by_name_en_query(name_en: str) -> DictRow:
    """
    Retrieves a user space by its name_en.
    """
    query = "SELECT * FROM userspace WHERE name_en=%s AND status=%s"
    return execute_query(query, (name_en, True), fetch="one")


def get_user_spaces_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all user spaces by their user ID.
    """
    query = "SELECT * FROM userspace WHERE user_id=%s AND status=%s"
    return execute_query(query, (user_id, True), fetch="all")


def get_all_user_spaces_query() -> list:
    """
    Retrieves all user spaces.
    """
    query = "SELECT * FROM userspace WHERE status=%s"
    return execute_query(query, (True,), fetch="all")
