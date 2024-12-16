from datetime import datetime

from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_balance_table_query() -> None:
    """
    Creates a table for storing user balances.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS balance (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    for_month BOOLEAN DEFAULT FALSE,
    for_three_month BOOLEAN DEFAULT FALSE,
    for_six_month BOOLEAN DEFAULT FALSE,
    for_nine_month BOOLEAN DEFAULT FALSE,
    for_year BOOLEAN DEFAULT FALSE,
    status BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    starts_at DATE NOT NULL DEFAULT NOW(),
    ends_at DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW());""")
    return None


def insert_balance_query(user_id: int, ends_at, for_month: bool=False, for_three_month: bool=False,
                         for_six_month: bool=False, for_nine_month: bool=False, for_year: bool=False,
                         starts_at=None, is_active=True) -> None:
    """
    Inserts a new balance record into the balance table.
    """
    query = """
    INSERT INTO balance (user_id, for_month, for_three_month, for_six_month, for_nine_month, for_year, starts_at, ends_at, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (user_id, for_month, for_three_month, for_six_month, for_nine_month, for_year,
                          starts_at, ends_at, is_active))
    return None


def activate_balance_by_id_query(balance_id) -> None:
    """
    Activates a balance record by its ID.
    """
    query = "UPDATE balance SET is_active=%s WHERE id=%s"
    execute_query(query, (True, balance_id))
    return None


def deactivate_balance_by_id_query(balance_id) -> None:
    """
    Deactivates a balance record by its ID.
    """
    query = "UPDATE balance SET is_active=%s WHERE id=%s"
    execute_query(query, (False, balance_id))
    return None


def delete_balance_query(balance_id: int) -> None:
    """
    Deletes a balance record from the balance table.
    """
    query = "UPDATE balance SET status=%s WHERE id=%s"
    execute_query(query, (False, balance_id))
    return None


# GET --------------------------------------------------------------------------------
def get_balances_by_user_id_query(user_id: int) -> list:
    """
    Retrieves a balance record by its user ID.
    """
    query = "SELECT * FROM balance WHERE user_id=%s AND status=TRUE"
    return execute_query(query, (user_id,), fetch="all")


def get_active_balance_by_user_id_query(user_id) -> DictRow:
    """
    Retrieves the active balance record by its user ID.
    """
    query = "SELECT * FROM balance WHERE user_id=%s AND is_active=TRUE AND status=TRUE"
    return execute_query(query, (user_id,), fetch="one")


def get_last_balance_by_user_id_query(user_id: int) -> DictRow:
    """
    Retrieves the last balance record by its user ID.
    """
    query = "SELECT * FROM balance WHERE user_id=%s ORDER BY starts_at DESC LIMIT 1"
    return execute_query(query, (user_id,), fetch="one")


def get_balance_by_id_query(balance_id: int) -> DictRow:
    """
    Retrieves a balance record by its ID.
    """
    query = "SELECT * FROM balance WHERE id=%s AND status=TRUE"
    return execute_query(query, (balance_id,), fetch="one")


def get_balance_by_starts_at_query(starts_at: str) -> DictRow:
    """
    Retrieves a balance record by its start date.
    """
    query = "SELECT * FROM balance WHERE starts_at=%s AND status=TRUE"
    return execute_query(query, (starts_at,), fetch="one")


def get_balance_by_ends_at_query(ends_at: str) -> DictRow:
    """
    Retrieves a balance record by its end date.
    """
    query = "SELECT * FROM balance WHERE ends_at=%s AND status=TRUE"
    return execute_query(query, (ends_at,), fetch="one")


def get_all_balance_query() -> list:
    """
    Retrieves all balance records.
    """
    query = "SELECT * FROM balance WHERE status=TRUE ORDER BY id DESC"
    return execute_query(query, fetch="all")


def get_all_active_balance_query() -> list:
    """
    Retrieves all active balance records from the database where both is_active and status are TRUE.
    """
    query = """
        SELECT * 
        FROM balance 
        WHERE is_active = TRUE 
        AND status = TRUE 
        ORDER BY ends_at
    """
    return execute_query(query, fetch="all")


def get_all_future_active_balance_query() -> list:
    """
    Retrieves all active balance records from the database where both is_active and status are TRUE.
    """
    query = """
        SELECT *
        FROM balance
        WHERE is_active = FALSE AND starts_at = %s
        AND status = TRUE
        ORDER BY starts_at
    """
    return execute_query(query, (datetime.date(datetime.now()),), fetch="all")
