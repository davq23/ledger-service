from config.config import app_config
from redis import Redis

redis_client = Redis(
    host=app_config['REDIS_HOST'],
    port=app_config['REDIS_PORT'],
    db=0,
    password=app_config['REDIS_PASSWORD'],
    decode_responses=True
)