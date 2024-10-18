from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_i2c_table_query() -> None:
    """
    Creates a table for storing I2C devices.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS i2c (
        id BIGSERIAL PRIMARY KEY,
        name_uz TEXT NOT NULL,
        name_ru TEXT NOT NULL,
        name_en TEXT NOT NULL,
        chipset_id BIGINT REFERENCES chipset(id),
        user_id BIGINT REFERENCES users(id),
        category_id BIGINT REFERENCES i2c_category(id),
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_i2c_query(name_uz: str, name_ru: str, name_en: str, chipset_id: int, user_id: int, category_id: int) -> None:
    """
    Inserts a new I2C device into the i2c_device table.
    """
    query = """
    INSERT INTO i2c (name_uz, name_ru, name_en, chipset_id, user_id, category_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (name_uz, name_ru, name_en, chipset_id, user_id, category_id))
    return None


def update_i2c_query(id_of: int, new_name_uz: str, new_name_ru: str, new_name_en: str, chipset_id: int,
                     user_id: int, category_id: int) -> None:
    """
    Updates an I2C device.
    """
    query = """
    UPDATE i2c
    SET name_uz=%s, name_ru=%s, name_en=%s, chipset_id=%s, user_id=%s, category_id=%s, updated_at=%s
    WHERE id=%s
    """
    execute_query(query, (new_name_uz, new_name_ru, new_name_en, chipset_id, user_id,
                          category_id, datetime.now(), id_of))
    return None


def delete_i2c_query(id_of: int) -> None:
    """
    Deletes an I2C device from the i2c_device table.
    """
    query = "UPDATE i2c SET status=%s WHERE id=%s"
    execute_query(query, (False, id_of))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_i2c_by_id_query(id_of) -> DictRow:
    """
    Retrieves an I2C device by its ID.
    """
    query = "SELECT * FROM i2c WHERE id=%s AND status=%s"
    return execute_query(query, (id_of, True), fetch="one")


def get_i2c_by_name_uz_query(name_uz: str) -> DictRow:
    """
    Retrieves an I2C device by its name_uz.
    """
    query = "SELECT * FROM i2c WHERE name_uz=%s AND status=%s"
    return execute_query(query, (name_uz, True), fetch="one")


def get_i2c_by_name_ru_query(name_ru: str) -> DictRow:
    """
    Retrieves an I2C device by its name_ru.
    """
    query = "SELECT * FROM i2c WHERE name_ru=%s AND status=%s"
    return execute_query(query, (name_ru, True), fetch="one")


def get_i2c_by_name_en_query(name_en: str) -> DictRow:
    """
    Retrieves an I2C device by its name_en.
    """
    query = "SELECT * FROM i2c WHERE name_en=%s AND status=%s"
    return execute_query(query, (name_en, True), fetch="one")


def get_all_i2cs_by_chipset_id_query(chipset_id: int) -> list:
    """
    Retrieves all I2C devices associated with a specific chipset ID.
    """
    query = "SELECT * FROM i2c WHERE chipset_id=%s AND status=%s"
    return execute_query(query, (chipset_id, True), fetch="all")


def get_all_i2cs_by_category_id_query(category_id: int) -> list:
    """
    Retrieves all I2C devices associated with a specific category ID.
    """
    query = "SELECT * FROM i2c WHERE category_id=%s AND status=%s"
    return execute_query(query, (category_id, True), fetch="all")


def get_all_i2cs_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all I2C devices associated with a specific user ID.
    """
    query = "SELECT * FROM i2c WHERE user_id=%s AND status=%s"
    return execute_query(query, (user_id, True), fetch="all")


def get_i2c_by_category_and_chipset_query(category_id: int, chipset_id: int) -> DictRow:
    """
    Retrieves an I2C device by its category ID and chipset ID.
    """
    query = "SELECT * FROM i2c WHERE category_id=%s AND chipset_id=%s AND status=%s"
    return execute_query(query, (category_id, chipset_id, True), fetch="one")


def get_all_i2cs_query() -> list:
    """
    Retrieves all I2C devices.
    """
    query = "SELECT * FROM i2c WHERE status=%s"
    return execute_query(query, (True,), fetch="all")
