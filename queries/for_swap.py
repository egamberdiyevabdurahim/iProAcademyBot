from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_swap_table_query() -> None:
    """
    Creates a table for storing swap requests.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS swap (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    model_id BIGINT REFERENCES model(id),
    title VARCHAR(255) NOT NULL,
    name_uz VARCHAR(255),
    name_ru VARCHAR(255),
    name_en VARCHAR(255),
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW())""")
    return None


def insert_swap_query(user_id: int, model_id: int, title: str, name_uz: str, name_ru: str, name_en: str):
    """
    Inserts a new swap request into the swap table.
    """
    query = """
    INSERT INTO swap (user_id, model_id, title, name_uz, name_ru, name_en)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    return execute_query(query, (user_id, model_id, title, name_uz, name_ru, name_en), fetch="return")


def update_swap_query(swap_id: int, title: str, name_uz: str, name_ru: str, name_en: str, model_id) -> None:
    """
    Updates a swap request.
    """
    query = """
    UPDATE swap
    SET title=%s, name_uz=%s, name_ru=%s, name_en=%s, updated_at=NOW(), model_id=%s
    WHERE id=%s
    """
    execute_query(query, (title, name_uz, name_ru, name_en, model_id, swap_id))
    return None


def delete_swap_query(swap_id) -> None:
    """
    Deletes a swap request from the swap table.
    """
    execute_query("UPDATE swap SET status=%s WHERE id=%s", (False, swap_id))
    return None


# GET --------------------------------------------------------------------------------
def get_swap_by_id_query(swap_id) -> DictRow:
    """
    Retrieves a swap request by its ID.
    """
    query = "SELECT * FROM swap WHERE id=%s AND status=%s"
    return execute_query(query, (swap_id, True), fetch="one")


def get_swap_by_title_and_model_id_query(title: str, model_id):
    """
    Retrieves a swap request by its title and model ID.
    """
    query = "SELECT * FROM swap WHERE title=%s AND model_id=%s AND status=%s"
    return execute_query(query, (title, model_id, True), fetch="one")


def get_swaps_by_model_id_query(model_id) -> list:
    """
    Retrieves all swap requests by their model ID.
    """
    query = "SELECT * FROM swap WHERE model_id=%s AND status=%s"
    return execute_query(query, (model_id, True), fetch="all")


def get_swaps_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all swap requests by their user ID.
    """
    query = "SELECT * FROM swap WHERE user_id=%s AND status=%s"
    return execute_query(query, (user_id, True), fetch="all")


def get_all_swaps_query() -> list:
    """
    Retrieves all swap requests.
    """
    return execute_query("SELECT * FROM swap WHERE status=TRUE", fetch="all")