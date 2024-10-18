from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_panic_array_table_query() -> None:
    """
    Creates a table for storing panic arrays.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS panic_array (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_panic_array_query(name: str) -> None:
    """
    Inserts a new panic array into the panic_array table.
    """
    query = """
    INSERT INTO panic_array (name)
    VALUES (%s)
    """
    execute_query(query, (name,))
    return None


def update_panic_array_name_query(panic_array_id: int, new_name: str) -> None:
    """
    Updates the name of a panic array.
    """
    query = "UPDATE panic_array SET name=%s WHERE id=%s"
    execute_query(query, (new_name, panic_array_id))
    return None


def delete_panic_array_query(panic_array_id: int) -> None:
    """
    Deletes a panic array from the panic_array table.
    """
    query = "DELETE FROM panic_array WHERE id=%s"
    execute_query(query, (panic_array_id,))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_panic_array_by_id_query(panic_array_id) -> DictRow:
    """
    Retrieves a panic array by its ID.
    """
    query = "SELECT * FROM panic_array WHERE id=%s"
    return execute_query(query, (panic_array_id,), fetch="one")


def get_panic_array_by_name_query(name: str) -> DictRow:
    """
    Retrieves a panic array by its name.
    """
    query = "SELECT * FROM panic_array WHERE name=%s"
    return execute_query(query, (name,), fetch="one")


def get_all_panic_arrays_query() -> list:
    """
    Retrieves all panic arrays.
    """
    query = "SELECT * FROM panic_array ORDER BY id"
    return execute_query(query, fetch="all")
