import os
from dotenv import load_dotenv

load_dotenv()

app_config = {
    'DB_USERNAME': os.environ.get('DB_USERNAME'),
    'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
    'DB_HOST': os.environ.get('DB_HOST'),
    'DB_NAME': os.environ.get('DB_NAME'),
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'APP_MODE': os.environ.get('APP_MODE')
}