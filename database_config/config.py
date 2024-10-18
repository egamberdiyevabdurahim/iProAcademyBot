import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DB_CONFIG = {
    'database': DB_NAME,
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT,
}


TOKEN = os.getenv('TOKEN')


FIRST_API_URL = os.getenv('FIRST_API_URL')
FIRST_API_USER = os.getenv('FIRST_API_USER')
FIRST_API_KEY = os.getenv('FIRST_API_KEY')


GROUP_ID = os.getenv('GROUP_ID')