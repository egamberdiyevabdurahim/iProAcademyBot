from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_activity_table_query() -> None:
    """
    Creates a table for storing user activities.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS activity (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL REFERENCES users(id),
        text TEXT,
        with_id TEXT,
        created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """)
    return None


def insert_activity_query(user_id: int, text: str = None, with_id = None) -> None:
    """
    Inserts a new activity into the activity table.
    """
    execute_query("""
    INSERT INTO activity (user_id, text, with_id)
    VALUES (%s, %s, %s);
    """, (user_id, text, with_id))
    return None



# GET ----------------------------------------------------------------------------
def get_activity_by_id_query(id_of: int) -> DictRow:
    """
    Retrieves an activity by its ID.
    """
    query = """
    SELECT *
    FROM activity
    WHERE id = %s
    """
    return execute_query(query, (id_of,), fetch='one')


def get_activities_by_user_id_query(user_id: str) -> list:
    """
    Gets activities for a specific user.
    """
    query = """
    SELECT *
    FROM activity
    WHERE user_id = %s
    ORDER BY created_at DESC;
    """
    return execute_query(query, (user_id,), 'all')


def get_all_activities_query() -> list:
    """
    Gets all activities.
    """
    query = """
    SELECT *
    FROM activity
    ORDER BY created_at DESC;
    """
    return execute_query(query, fetch='all')


def get_last_activity_by_user_id_query(user_id) -> DictRow:
    """
    Retrieves the last activity record by its user ID.
    """
    query = "SELECT * FROM activity WHERE user_id=%s ORDER BY created_at DESC LIMIT 1"
    return execute_query(query, (user_id,), fetch="one")


def get_yesterdays_first_activity_by_user_id_query(user_id) -> DictRow:
    """
    Retrieves the first activity record of the previous day by its user ID.
    """
    query = ("SELECT * FROM activity WHERE user_id=%s AND created_at >= NOW() - INTERVAL '1 day' "
             "ORDER BY created_at ASC "
             "LIMIT 1")
    return execute_query(query, (user_id,), fetch="one")
