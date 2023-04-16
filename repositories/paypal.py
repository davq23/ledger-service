
from redis import Redis


def get_paypal_auth_token(redis_client: Redis):
    return redis_client.get('PAYPAL_AUTH_TOKEN')

def set_paypal_auth_token(redis_client: Redis, auth_token: str, expires_in: int):
    redis_client.set('PAYPAL_AUTH_TOKEN', auth_token, ex=expires_in)