from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_i2c_category_table_query() -> None:
    """
    Creates a table for storing I2C categories.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS i2c_category (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(64) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_i2c_category_query(name: str) -> None:
    """
    Inserts a new I2C category into the i2c_category table.
    """
    query = """
    INSERT INTO i2c_category (name)
    VALUES (%s)
    """
    execute_query(query, (name,))
    return None


def update_i2c_category_query(category_id: int, name: str) -> None:
    """
    Updates an I2C category.
    """
    query = """
    UPDATE i2c_category
    SET name=%s
    WHERE id=%s
    """
    execute_query(query, (name, category_id))
    return None


def delete_i2c_category_query(category_id: int) -> None:
    """
    Deletes an I2C category from the i2c_category table.
    """
    query = "DELETE FROM i2c_category WHERE id=%s"
    execute_query(query, (category_id,))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_i2c_category_by_id_query(category_id: int) -> DictRow:
    """
    Retrieves an I2C category by its ID.
    """
    query = "SELECT * FROM i2c_category WHERE id=%s"
    return execute_query(query, (category_id,), fetch="one")


def get_i2c_category_by_name_query(name: str) -> DictRow:
    """
    Retrieves an I2C category by its name.
    """
    query = "SELECT * FROM i2c_category WHERE name=%s"
    return execute_query(query, (name,), fetch="one")


def get_all_i2c_categories_query() -> list:
    """
    Retrieves all I2C categories.
    """
    query = "SELECT * FROM i2c_category"
    return execute_query(query, fetch="all")
