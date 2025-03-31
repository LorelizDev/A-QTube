import redis

from shared.utils.logger import setup_logger

logger = setup_logger()

REDIS_URL = "redis://localhost:6379"
redis_client = redis.from_url(REDIS_URL)


def get_from_cache(key):
    try:
        logger.info(f"Buscando en caché: {key}")
        cached_value = redis_client.get(key)
        if cached_value:
            logger.info("Valor encontrado en caché.")
            return cached_value.decode("utf-8")
        logger.info("No se encontró valor en caché.")
        return None
    except Exception as e:
        logger.error(f"Error al acceder a Redis: {str(e)}")
        raise


def save_to_cache(key, value):
    try:
        logger.info(f"Guardando en caché: {key}")
        redis_client.set(key, value)
        logger.info("Valor guardado en caché.")
    except Exception as e:
        logger.error(f"Error al guardar en Redis: {str(e)}")
        raise
