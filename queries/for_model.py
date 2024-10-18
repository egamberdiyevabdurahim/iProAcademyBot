from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_model_table_query() -> None:
    """
    Creates a table for storing models.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS model (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW())""")
    return None


def insert_model_query(name: str) -> None:
    """
    Inserts a new model into the model table.
    """
    execute_query("INSERT INTO model (name) VALUES (%s)", (name,))
    return None


def update_model_query(mode_id, new_name) -> None:
    """
    Updates the name of a model.
    """
    execute_query("UPDATE model SET name=%s, updated_at=NOW() WHERE id=%s", (new_name, mode_id))
    return None


def delete_model_query(model_id: int) -> None:
    """
    Deletes a model from the model table.
    """
    execute_query("UPDATE model SET status=%s WHERE id=%s", (False, model_id))
    return None


# GET --------------------------------------------------------------------------
def get_model_by_id_query(model_id) -> DictRow:
    """
    Retrieves a model by its ID.
    """
    query = "SELECT * FROM model WHERE id=%s"
    return execute_query(query, (model_id,), fetch="one")


def get_model_by_name_query(name: str) -> DictRow:
    """
    Retrieves a model by its name.
    """
    query = "SELECT * FROM model WHERE name=%s"
    return execute_query(query, (name,), fetch="one")


def get_all_models_query() -> list[DictRow]:
    """
    Retrieves all models.
    """
    return execute_query("SELECT * FROM model WHERE status=TRUE", fetch="all")