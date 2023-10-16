import json
import redis
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb

# Global Redis connection pool
REDIS_CONNECTION_POOL = None
# Redis hash key for buffering
REDIS_BUFFER_KEY = "redis_buffer"


def _get_pool():
    """
    Get the Redis connection pool, initialize if not already done.
    """
    global REDIS_CONNECTION_POOL
    if REDIS_CONNECTION_POOL is None:
        config_obj = get_config_instance()
        REDIS_CONNECTION_POOL = redis.ConnectionPool(
            host=config_obj.get_config("redis_host"),
            port=int(config_obj.get_config("redis_port")),
            decode_responses=True
        )
    return REDIS_CONNECTION_POOL


def _load_buffer_file(key):
    """
    Load an item from the buffer using Redis.
    """
    rrdis = redis.Redis(connection_pool=_get_pool())

    if rrdis.hexists(REDIS_BUFFER_KEY, key):
        return json.loads(rrdis.hget(REDIS_BUFFER_KEY, key))

    raise Exception("Buffer item not found for the given key.")


def _save_buffer_file(lists):
    """
    Save a list of items to the Redis buffer.
    """
    rrdis = redis.Redis(connection_pool=_get_pool())
    for key, value in lists:
        rrdis.hset(REDIS_BUFFER_KEY, key, json.dumps(value))


def _delete_buffer_file(key):
    """
    Delete a buffer item from Redis based on the key.
    """
    if _has_buffer_file(key):
        rrdis = redis.Redis(connection_pool=_get_pool())
        rrdis.hdel(REDIS_BUFFER_KEY, key)


def _has_buffer_file(key):
    """
    Check if a buffer item exists in Redis for the given key.
    """
    rrdis = redis.Redis(connection_pool=_get_pool())
    return rrdis.hexists(REDIS_BUFFER_KEY, key)


# Update bufferbase with the implemented functions
bb.has_buffer_file = _has_buffer_file
bb.load_buffer_file = _load_buffer_file
bb.delete_buffer_file = _delete_buffer_file
bb.save_buffer_file = _save_buffer_file
