from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_itunes_table_query() -> None:
    """
    Creates a table for storing itunes requests.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS itunes (
    id BIGSERIAL PRIMARY KEY,
    name_uz VARCHAR(255) NOT NULL,
    name_ru VARCHAR(255) NOT NULL,
    name_en VARCHAR(255) NOT NULL,
    error_code VARCHAR(255) NOT NULL,
    user_id BIGINT REFERENCES users(id),
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW())""")
    return None


def insert_itunes_query(name_uz: str, name_ru: str, name_en: str, error_code: str, user_id: int) -> None:
    """
    Inserts a new itunes request into the itunes table.
    """
    execute_query("""
    INSERT INTO itunes (name_uz, name_ru, name_en, error_code, user_id)
    VALUES (%s, %s, %s, %s, %s)
    """, (name_uz, name_ru, name_en, error_code, user_id))
    return None


def update_itunes_query(itunes_id: int, new_name_uz: str, new_name_ru: str, new_name_en: str, new_error_code: str) -> None:
    """
    Updates an itunes request.
    """
    execute_query("""
    UPDATE itunes
    SET name_uz=%s, name_ru=%s, name_en=%s, error_code=%s, updated_at=NOW()
    WHERE id=%s
    """, (new_name_uz, new_name_ru, new_name_en, new_error_code, itunes_id))
    return None


def delete_itunes_query(itunes_id: int) -> None:
    """
    Deletes an itunes request from the itunes table.
    """
    execute_query("UPDATE itunes SET status=%s WHERE id=%s", (False, itunes_id))
    return None


# GET --------------------------------------------------------------------------------
def get_itunes_by_id_query(itunes_id: int) -> DictRow:
    """
    Retrieves an itunes request by its ID.
    """
    query = "SELECT * FROM itunes WHERE id=%s AND status=%s"
    return execute_query(query, (itunes_id, True), fetch="one")


def get_itunes_by_name_uz_query(name: str) -> list:
    """
    Retrieves an itunes request by its name.
    """
    query = "SELECT * FROM itunes WHERE name_uz=%s AND status=%s"
    return execute_query(query, (name, True), fetch="all")


def get_itunes_by_name_ru_query(name: str) -> list:
    """
    Retrieves an itunes request by its name in Russian.
    """
    query = "SELECT * FROM itunes WHERE name_ru=%s AND status=%s"
    return execute_query(query, (name, True), fetch="all")


def get_itunes_by_name_en_query(name: str) -> list:
    """
    Retrieves an itunes request by its name in English.
    """
    query = "SELECT * FROM itunes WHERE name_en=%s AND status=%s"
    return execute_query(query, (name, True), fetch="all")


def get_itunes_by_error_code_query(error_code: str) -> DictRow:
    """
    Retrieves all itunes requests by their error code.
    """
    print(error_code)
    query = "SELECT * FROM itunes WHERE error_code=%s AND status=%s"
    return execute_query(query, (error_code, True), fetch="one")


def get_all_itunes_query() -> list:
    """
    Retrieves all itunes requests.
    """
    return execute_query("SELECT * FROM itunes WHERE status=TRUE", fetch="all")