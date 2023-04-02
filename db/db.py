import psycopg2
from config.config import app_config

db_connection = psycopg2.connect(
    dsn=f"postgresql://{app_config['DB_USERNAME']}:{app_config['DB_PASSWORD']}@{app_config['DB_HOST']}/{app_config['DB_NAME']}"
)
