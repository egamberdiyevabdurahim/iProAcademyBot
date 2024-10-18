from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_chipset_table_query() -> None:
    """
    Creates a table for storing chipsets.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS chipset (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_chipset_query(name: str) -> None:
    """
    Inserts a new chipset into the chipset table.
    """
    query = """
    INSERT INTO chipset (name)
    VALUES (%s)
    """
    execute_query(query, (name,))
    return None


def update_chipset_query(chipset_id: int, name: str) -> None:
    """
    Updates a chipset.
    """
    query = """
    UPDATE chipset
    SET name=%s
    WHERE id=%s
    """
    execute_query(query, (name, chipset_id))
    return None


def delete_chipset_query(chipset_id: int) -> None:
    """
    Deletes a chipset from the chipset table.
    """
    query = "DELETE FROM chipset WHERE id=%s"
    execute_query(query, (chipset_id,))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_chipset_by_id_query(chipset_id) -> DictRow:
    """
    Retrieves a chipset by its ID.
    """
    query = "SELECT * FROM chipset WHERE id=%s"
    return execute_query(query, (chipset_id,), fetch="one")


def get_chipset_by_name_query(name: str) -> DictRow:
    """
    Retrieves a chipset by its name.
    """
    query = "SELECT * FROM chipset WHERE name=%s"
    return execute_query(query, (name,), fetch="one")


def get_all_chipsets_query() -> list:
    """
    Retrieves all chipsets.
    """
    query = "SELECT * FROM chipset"
    return execute_query(query, fetch="all")
