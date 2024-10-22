from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_imei_866_table_query() -> None:
    """
    Creates a table for storing 866 IMEI numbers.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS imei_866 (
    id SERIAL PRIMARY KEY,
    imei VARCHAR(15) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT REFERENCES users(id))""")
    return None


def insert_imei_866_query(imei: str, user_id) -> None:
    """
    Inserts a new 866 IMEI number into the table.
    """
    execute_query("INSERT INTO imei_866 (imei, user_id) VALUES (%s, %s)", (imei, user_id))
    return None


def get_all_imei_866_by_user_id(user_id) -> list:
    """
    Retrieves all 866 IMEI numbers by their user ID.
    """
    query = "SELECT * FROM imei_866 WHERE user_id=%s ORDER BY created_at DESC"
    return execute_query(query, (user_id,), fetch="all")


def get_imei_866_by_id_query(imei_id) -> DictRow:
    """
    Retrieves a 866 IMEI number by its ID.
    """
    query = "SELECT * FROM imei_866 WHERE id=%s"
    return execute_query(query, (imei_id,), fetch="one")


def get_imei_866_by_imei_query(imei) -> DictRow:
    """
    Retrieves a 866 IMEI number by its IMEI.
    """
    query = "SELECT * FROM imei_866 WHERE imei=%s"
    return execute_query(query, (imei,), fetch="one")

# ----------------------------------------------------------------------------------- #

def create_imei_860_table_query() -> None:
    """
    Creates a table for storing 860 IMEI numbers.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS imei_860 (
    id SERIAL PRIMARY KEY,
    imei VARCHAR(15) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT REFERENCES users(id))""")
    return None


def insert_imei_860_query(imei: str, user_id) -> None:
    """
    Inserts a new 860 IMEI number into the table.
    """
    execute_query("INSERT INTO imei_860 (imei, user_id) VALUES (%s, %s)", (imei, user_id))
    return None


def get_all_imei_860_by_user_id(user_id) -> list:
    """
    Retrieves all 860 IMEI numbers by their user ID.
    """
    query = "SELECT * FROM imei_860 WHERE user_id=%s ORDER BY created_at DESC"
    return execute_query(query, (user_id,), fetch="all")


def get_imei_860_by_id_query(imei_id) -> DictRow:
    """
    Retrieves a 860 IMEI number by its ID.
    """
    query = "SELECT * FROM imei_860 WHERE id=%s"
    return execute_query(query, (imei_id,), fetch="one")


def get_imei_860_by_imei_query(imei) -> DictRow:
    """
    Retrieves a 860 IMEI number by its IMEI.
    """
    query = "SELECT * FROM imei_860 WHERE imei=%s"
    return execute_query(query, (imei,), fetch="one")

# ----------------------------------------------------------------------------------- #

def create_imei_355_table_query() -> None:
    """
    Creates a table for storing 355 IMEI numbers.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS imei_355 (
    id SERIAL PRIMARY KEY,
    imei VARCHAR(15) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT REFERENCES users(id))""")
    return None


def insert_imei_355_query(imei: str, user_id) -> None:
    """
    Inserts a new 355 IMEI number into the table.
    """
    execute_query("INSERT INTO imei_355 (imei, user_id) VALUES (%s, %s)", (imei, user_id))
    return None


def get_all_imei_355_by_user_id(user_id) -> list:
    """
    Retrieves all 355 IMEI numbers by their user ID.
    """
    query = "SELECT * FROM imei_355 WHERE user_id=%s ORDER BY created_at DESC"
    return execute_query(query, (user_id,), fetch="all")


def get_imei_355_by_id_query(imei_id) -> DictRow:
    """
    Retrieves a 355 IMEI number by its ID.
    """
    query = "SELECT * FROM imei_355 WHERE id=%s"
    return execute_query(query, (imei_id,), fetch="one")


def get_imei_355_by_imei_query(imei) -> DictRow:
    """
    Retrieves a 355 IMEI number by its IMEI.
    """
    query = "SELECT * FROM imei_355 WHERE imei=%s"
    return execute_query(query, (imei,), fetch="one")

# ----------------------------------------------------------------------------------- #

def create_imei_358_table_query() -> None:
    """
    Creates a table for storing 358 IMEI numbers.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS imei_358 (
    id SERIAL PRIMARY KEY,
    imei VARCHAR(15) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id BIGINT REFERENCES users(id))""")
    return None


def insert_imei_358_query(imei: str, user_id) -> None:
    """
    Inserts a new 358 IMEI number into the table.
    """
    execute_query("INSERT INTO imei_358 (imei, user_id) VALUES (%s, %s)", (imei, user_id))
    return None


def get_all_imei_358_by_user_id(user_id) -> list:
    """
    Retrieves all 358 IMEI numbers by their user ID.
    """
    query = "SELECT * FROM imei_358 WHERE user_id=%s ORDER BY created_at DESC"
    return execute_query(query, (user_id,), fetch="all")


def get_imei_358_by_id_query(imei_id) -> DictRow:
    """
    Retrieves a 358 IMEI number by its ID.
    """
    query = "SELECT * FROM imei_358 WHERE id=%s"
    return execute_query(query, (imei_id,), fetch="one")


def get_imei_358_by_imei_query(imei) -> DictRow:
    """
    Retrieves a 355 IMEI number by its IMEI.
    """
    query = "SELECT * FROM imei_358 WHERE imei=%s"
    return execute_query(query, (imei,), fetch="one")