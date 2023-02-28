import os

from dotenv import load_dotenv

load_dotenv()

# Database
DB_ENGINE = os.getenv("DB_ENGINE")
DB_NAME = os.getenv("DB_NAME", default="postgresql+psycopg2")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="adm")
DB_HOST = os.getenv("DB_HOST", default="localhost")
DB_PORT = os.getenv("DB_PORT", default="5432")

# bot
TOKEN = os.getenv("TG_BOT")

# Data
DATA_FILE = os.getenv("DATA")
