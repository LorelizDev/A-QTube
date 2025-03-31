import os

import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
redis_client = redis.from_url(REDIS_URL)


def get_from_cache(key):
    try:
        cached_value = redis_client.get(key)
        if cached_value:
            return cached_value.decode("utf-8")
        return None
    except Exception as e:
        print(f"Error al obtener de Redis: {str(e)}")
        raise


def save_to_cache(key, value):
    try:
        redis_client.set(key, value)
    except Exception as e:
        print(f"Error al guardar en Redis: {str(e)}")
        raise
