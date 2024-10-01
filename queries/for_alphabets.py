from psycopg2.extras import DictRow

from database_config.db_settings import execute_query


def create_alphabets_table_query() -> None:
    """
    Creates a table for storing alphabets.
    """
    execute_query("""
    CREATE TABLE IF NOT EXISTS alphabets (
        id BIGSERIAL PRIMARY KEY,
        name_uz TEXT NOT NULL,
        name_ru TEXT NOT NULL,
        name_en TEXT NOT NULL,
        code VARCHAR(64) NOT NULL,
        user_id BIGINT NOT NULL REFERENCES users(id),
        status BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    )""")
    return None


def insert_alphabet_query(name_uz: str, name_ru: str, name_en: str, code: str, user_id: int) -> None:
    """
    Inserts a new alphabet into the alphabets table.
    """
    query = """
    INSERT INTO alphabets (name_uz, name_ru, name_en, code, user_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(query, (name_uz, name_ru, name_en, code, user_id))
    return None


def update_alphabet_query(alphabet_id: int, new_name_uz: str, new_name_ru: str, new_name_en: str, new_code: str) -> None:
    """
    Updates the name or code of an alphabet.
    """
    query = """
    UPDATE alphabets
    SET name_uz=%s, name_ru=%s, name_en=%s, code=%s, updated_at=NOW()
    WHERE id=%s
    """
    execute_query(query, (new_name_uz, new_name_ru, new_name_en, new_code, alphabet_id))
    return None


def delete_alphabet_query(alphabet_id: int) -> None:
    """
    Deletes an alphabet from the alphabets table.
    """
    query = "UPDATE alphabets SET status=%s WHERE id=%s"
    execute_query(query, (False, alphabet_id))
    return None


# GET--------------------------------------------------------------------------------------------------
def get_alphabet_by_id_query(alphabet_id: int) -> DictRow:
    """
    Retrieves an alphabet by its ID.
    """
    query = """
    SELECT *
    FROM alphabets
    WHERE id=%s AND status=TRUE
    """
    return execute_query(query, (alphabet_id,), "one")


def get_alphabet_by_name_uz_query(name_uz: str) -> DictRow:
    """
    Retrieves an alphabet by its name_uz.
    """
    query = """
    SELECT *
    FROM alphabets
    WHERE name_uz=%s AND status=TRUE
    """
    return execute_query(query, (name_uz,), "one")


def get_alphabet_by_name_ru_query(name_ru: str) -> DictRow:
    """
    Retrieves an alphabet by its name_ru.
    """
    query = """
    SELECT *
    FROM alphabets
    WHERE name_ru=%s AND status=TRUE
    """
    return execute_query(query, (name_ru,), "one")


def get_alphabet_by_name_en_query(name_en: str) -> DictRow:
    """
    Retrieves an alphabet by its name_en.
    """
    query = """
    SELECT *
    FROM alphabets
    WHERE name_en=%s AND status=TRUE
    """
    return execute_query(query, (name_en,), "one")


def get_alphabets_by_first_letter_query(letter: str) -> list:
    """
    Fetches all alphabets from the 'alphabets' table that start with a given letter,
    where the alphabet status is TRUE, and orders them alphabetically by name.

    The LIKE operator is used to match characters in a column.
    The % character is a wildcard that matches any number of characters.
    """
    query = f"""
    SELECT *
    FROM alphabets
    WHERE code LIKE '{letter}%' AND status = TRUE
    ORDER BY code
    """
    return execute_query(query, fetch="all")


def get_alphabet_by_code_query(code: str) -> DictRow:
    """
    Retrieves an alphabet by its code.
    """
    query = """
    SELECT *
    FROM alphabets
    WHERE code=%s AND status=TRUE
    """
    return execute_query(query, (code,), "one")


def get_alphabets_by_user_id_query(user_id: int) -> list:
    """
    Retrieves all alphabets by their user ID.
    """
    query = "SELECT * FROM alphabets WHERE user_id=%s AND status=TRUE"
    return execute_query(query, (user_id,), "all")


def get_all_alphabets_query() -> list:
    """
    Retrieves all alphabets.
    """
    query = "SELECT * FROM alphabets WHERE status=TRUE"
    return execute_query(query, fetch="all")
