from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_swap_photo_table_query() -> None:
    """
    Creates a table for storing swap photo requests.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS swap_photo (
    id BIGSERIAL PRIMARY KEY,
    swap_id BIGINT REFERENCES swap(id),
    photo_id VARCHAR(255) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW())""")
    return None


def insert_swap_photo_query(swap_id: int, photo_id: str) -> None:
    """
    Inserts a new swap photo request into the swap_photo table.
    """
    execute_query("INSERT INTO swap_photo (swap_id, photo_id) VALUES (%s, %s)", (swap_id, photo_id))
    return None


def delete_swap_photo_query(swap_photo_id: int) -> None:
    """
    Deletes a swap photo request from the swap_photo table.
    """
    execute_query("UPDATE swap_photo SET status=%s WHERE id=%s", (False, swap_photo_id))
    return None


# GET --------------------------------------------------------------------------------
def get_swap_photo_by_id_query(swap_photo_id: int) -> DictRow:
    """
    Retrieves a swap photo request by its ID.
    """
    query = "SELECT * FROM swap_photo WHERE id=%s AND status=%s"
    return execute_query(query, (swap_photo_id, True), fetch="one")


def get_swap_photos_by_swap_id_query(swap_id: int) -> list:
    """
    Retrieves all swap photo requests by their swap ID.
    """
    query = "SELECT * FROM swap_photo WHERE swap_id=%s AND status=%s"
    return execute_query(query, (swap_id, True), fetch="all")


def get_all_swap_photos_query() -> list[DictRow]:
    """
    Retrieves all swap photo requests.
    """
    return execute_query("SELECT * FROM swap_photo WHERE status=TRUE", fetch="all")