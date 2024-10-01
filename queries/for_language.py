from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_language_table_query() -> None:
    """
    Creates a table for storing languages.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS language (
        id SERIAL PRIMARY KEY,
        name VARCHAR(64) NOT NULL UNIQUE
    )""")
    return None


def insert_language_query(name: str) -> None:
    """
    Inserts a new language into the language table.
    """
    query = """
    INSERT INTO language (name)
    VALUES (%s)
    """
    execute_query(query, (name,))
    return None


def update_language_query(language_id: int, new_name: str) -> None:
    """
    Updates the name of a language.
    """
    query = "UPDATE language SET name=%s WHERE id=%s"
    execute_query(query, (new_name, language_id))
    return None


def delete_language_query(language_id: int) -> None:
    """
    Deletes a language from the language table.
    """
    query = "DELETE FROM language WHERE id=%s"
    execute_query(query, (language_id,))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_language_by_id_query(language_id: int) -> DictRow:
    """
    Retrieves a language by its ID.
    """
    query = "SELECT * FROM language WHERE id=%s"
    return execute_query(query, (language_id,), fetch="one")


def get_language_by_name_query(name: str) -> DictRow:
    """
    Retrieves a language by its name.
    """
    query = "SELECT * FROM language WHERE name=%s"
    return execute_query(query, (name.lower(),), fetch="one")


def get_all_languages_query() -> list:
    """
    Retrieves all languages.
    """
    query = "SELECT * FROM language"
    return execute_query(query, fetch="all")
