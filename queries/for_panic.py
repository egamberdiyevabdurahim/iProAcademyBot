from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_panic_table_query() -> None:
    """
    Creates a table for storing panic notifications.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS panic (
    id BIGSERIAL PRIMARY KEY,
    name_uz TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    name_en TEXT NOT NULL,
    photo TEXT,
    code VARCHAR(64) NOT NULL,
    array_id BIGINT REFERENCES panic_array(id),
    user_id BIGINT REFERENCES users(id),
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_panic_query(name_uz: str, name_ru: str, name_en: str, code: str,
                       array_id: int, user_id: int, photo=None) -> None:
    """
    Inserts a new panic notification into the panic table.
    """
    query = """
    INSERT INTO panic (name_uz, name_ru, name_en, code, array_id, user_id, photo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (name_uz, name_ru, name_en, code, array_id, user_id, photo))
    return None


def update_panic_query(panic_id: int, new_name_uz: str, new_name_ru: str, new_name_en: str,
                       code: str, array_id: int, new_photo=None) -> None:
    """
    Updates a panic notification.
    """
    query = ("""
    UPDATE panic
    SET name_uz=%s, name_ru=%s, name_en=%s, code=%s, array_id=%s, updated_at=%s, photo=%s
    WHERE id=%s AND status=%s""")
    execute_query(query, (new_name_uz, new_name_ru, new_name_en, code, array_id, datetime.now(),
                          new_photo, panic_id, True))
    return None


def delete_panic_query(panic_id: int) -> None:
    """
    Deletes a panic notification from the panic table.
    """
    query = "UPDATE panic SET status=%s WHERE id=%s"
    execute_query(query, (False, panic_id))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_panic_by_id_query(panic_id: int) -> DictRow:
    """
    Retrieves a panic notification by its ID.
    """
    query = "SELECT * FROM panic WHERE id=%s AND status=%s"
    return execute_query(query, (panic_id, True), fetch="one")


def get_panic_by_code_query(code: str) -> DictRow:
    """
    Retrieves a panic notification by its code.
    """
    query = "SELECT * FROM panic WHERE code=%s AND status=%s"
    return execute_query(query, (code, True), fetch="one")


def get_panic_by_name_uz_query(name_uz: str) -> DictRow:
    """
    Retrieves a panic notification by its name.
    """
    query = "SELECT * FROM panic WHERE name_uz=%s AND status=%s"
    return execute_query(query, (name_uz, True), fetch="one")


def get_panic_by_name_ru_query(name_ru: str) -> DictRow:
    """
    Retrieves a panic notification by its name in Russian.
    """
    query = "SELECT * FROM panic WHERE name_ru=%s AND status=%s"
    return execute_query(query, (name_ru, True), fetch="one")


def get_panic_by_name_en_query(name_en: str) -> DictRow:
    """
    Retrieves a panic notification by its name in English.
    """
    query = "SELECT * FROM panic WHERE name_en=%s AND status=%s"
    return execute_query(query, (name_en, True), fetch="one")


def get_all_panics_by_array_id_query(array_id: int) -> list:
    """
    Retrieves all panic notifications by their array ID.
    """
    query = "SELECT * FROM panic WHERE array_id=%s AND status=%s"
    return execute_query(query, (array_id, True), fetch="all")


def get_all_panics_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all panic notifications by their user ID.
    """
    query = "SELECT * FROM panic WHERE user_id=%s AND status=%s"
    return execute_query(query, (user_id, True), fetch="all")


def get_all_panics_query() -> list:
    """
    Retrieves all panic notifications.
    """
    query = "SELECT * FROM panic WHERE status=%s"
    return execute_query(query, (True,), fetch="all")
