import os

from database_config.db_settings import execute_query
from queries.for_balance import create_balance_table_query

from queries.for_pending_users import create_pending_user_table_query
from queries.for_users import create_users_table_query
# from queries.for_used import create_used_table_query
from queries.for_panic_array import create_panic_array_table_query
from queries.for_panic import create_panic_table_query
from queries.for_userspace import create_userspace_table_query
from queries.for_i2c_category import create_i2c_category_table_query
from queries.for_chipset import create_chipset_table_query
from queries.for_i2c import create_i2c_table_query
from queries.for_aop_panic import create_aop_panic_table_query
from queries.for_alphabets import create_alphabets_table_query
from queries.for_activity import create_activity_table_query

def create_is_used_table_query() -> None:
    """
    Creates a new table for tracking whether the application is already run.
    """
    query = """
        CREATE TABLE IF NOT EXISTS is_used (
            id BIGSERIAL PRIMARY KEY,
            is_used BOOLEAN DEFAULT FALSE
        );
    """
    execute_query(query)
    return None


def insert_is_used_query():
    """
    Inserts a new record into the is_used table.
    """
    query = """
        SELECT * FROM is_used
        ORDER BY id DESC
        LIMIT 1;
        """
    data = execute_query(query, fetch="one")
    if data is None:
        query = "INSERT INTO is_used (is_used) VALUES (False);"
        execute_query(query)
    return None


def update_is_used_query():
    """
    Updates the is_used column in the is_used table.
    """
    query = "UPDATE is_used SET is_used = TRUE;"
    execute_query(query)
    return None


def is_used():
    query = """
    SELECT * FROM is_used
    ORDER BY id
    LIMIT 1;
    """
    data = execute_query(query, fetch="one")
    return data['is_used'] is True


def before_run() -> None:
    """
    Creates all required tables before running the application.
    """
    create_pending_user_table_query()
    create_users_table_query()
    # create_used_table_query()
    create_panic_array_table_query()
    create_panic_table_query()
    create_userspace_table_query()
    create_i2c_category_table_query()
    create_chipset_table_query()
    create_i2c_table_query()
    create_aop_panic_table_query()
    create_alphabets_table_query()
    create_activity_table_query()
    create_balance_table_query()
    return None


def if_not_used():
    path = os.path.dirname(os.path.abspath(__file__))  # Get absolute path
    create_is_used_table_query()
    insert_is_used_query()

    if not is_used():
        before_run()

        # Read and execute SQL for category insertion
        # with open(os.path.join(path, 'inserter_for_languages.sql'), 'r') as insert_file:
        #     for line in insert_file:
        #         query = line.strip()
        #         execute_query(query)
        #
        # # Read and execute SQL for region insertion
        # with open(os.path.join(path, 'inserter_for_region.sql'), 'r') as insert_file:
        #     for line in insert_file:
        #         query = line.strip()
        #         execute_query(query)
        #
        # # Read and execute SQL for city insertion
        # with open(os.path.join(path, 'inserter_for_city.sql'), 'r') as insert_file:
        #     for line in insert_file:
        #         query = line.strip()
        #         execute_query(query)

        update_is_used_query()

    return None
