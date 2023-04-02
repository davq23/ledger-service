import os
from dotenv import load_dotenv

load_dotenv()

app_config = {
    'DB_USERNAME': os.environ.get('DB_USERNAME'),
    'DB_PASSWORD': os.environ.get('DB_PASSWORD'),
    'DB_HOST': os.environ.get('DB_HOST'),
    'DB_NAME': os.environ.get('DB_NAME'),
    'DB_PREFIX': os.environ.get('DB_PREFIX'),
    'APP_MODE': os.environ.get('APP_MODE'),
    'PAYPAL_REST_API_CLIENT_ID': os.environ.get('PAYPAL_REST_API_CLIENT_ID'),
    'PAYPAL_REST_API_CLIENT_SECRET': os.environ.get('PAYPAL_REST_API_CLIENT_SECRET'),
    'PAYPAL_REST_API_TIMEOUT': os.environ.get('PAYPAL_REST_API_TIMEOUT'),
    'PAYPAL_REST_API_URL': os.environ.get('PAYPAL_REST_API_URL'),
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
}

if app_config['DB_PREFIX'] is None:
    app_config['DB_PREFIX'] = ''

if app_config['PAYPAL_REST_API_TIMEOUT'] is not None:
    app_config['PAYPAL_REST_API_TIMEOUT'] = int(app_config['PAYPAL_REST_API_TIMEOUT'])
else:
    app_config['PAYPAL_REST_API_TIMEOUT'] = 10