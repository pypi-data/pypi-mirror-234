from functools import wraps
from tketool.hash_util import hash_str, hash_obj_strbase
import threading

BUFFER_ITEMS = {}
BUFFER_OPER_QUEUE = []

has_buffer_file = None
load_buffer_file = None
delete_buffer_file = None
save_buffer_file = None

flush_freq = 10

buffer_lock = threading.Lock()


def flush():
    """
        Flushes the buffer to the disk and clears the operation queue.
        """
    if has_buffer_file is None:
        raise Exception("No module imported")

    with buffer_lock:
        queue_set = set(BUFFER_OPER_QUEUE)
        save_item_list = [(key, BUFFER_ITEMS[key]) for key in queue_set]
        save_buffer_file(save_item_list)

        # Clear the queue after flushing
        BUFFER_OPER_QUEUE.clear()

def set_flush_freq(count):
    global flush_freq
    flush_freq = count


def _get_hash_key(func_name, *args, **kwargs):
    """
        Generate a unique hash key based on function name, arguments and keyword arguments.
    """

    key_buffer = [hash_str(func_name)]
    if args:
        key_buffer.append([hash_obj_strbase(arg) for arg in args])
    if kwargs:
        key_buffer.append([hash_obj_strbase(kwarg) for kwarg in kwargs.values()])
    return str(func_name) + "_" + hash_obj_strbase(key_buffer)


def buffer_item(key: str, value):
    """
    Cache an object.

    :param key: Key of the object.
    :param value: Value of the object.
    """
    with buffer_lock:
        nkey = _get_hash_key(key)
        BUFFER_ITEMS[nkey] = value
        BUFFER_OPER_QUEUE.append(nkey)

        if len(BUFFER_OPER_QUEUE) >= flush_freq:
            flush()


def get_buffer_item(key: str):
    """
   Retrieves a cached object.

   :param key: Key of the object.
   :return: The cached object. Raises an exception if not found.
   """

    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = _get_hash_key(key)
    with buffer_lock:
        if nkey in BUFFER_ITEMS:
            return BUFFER_ITEMS[nkey]

        if has_buffer_file(nkey):
            BUFFER_ITEMS[nkey] = load_buffer_file(nkey)
            return BUFFER_ITEMS[nkey]

    raise ValueError(f"No buffer item found for key: {key}")


def has_item_key(key: str):
    """
    Checks if a cached object exists for the given key.

    :param key: Key to check.
    :return: True if exists, otherwise False.
    """
    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = _get_hash_key(key)

    return nkey in BUFFER_ITEMS or has_buffer_file(nkey)


def remove_item(key: str):
    """
    Removes a cached object.

    :param key: Key of the object to remove.
    """
    if has_buffer_file is None:
        raise Exception("No module imported")

    nkey = _get_hash_key(key)

    with buffer_lock:
        if nkey in BUFFER_ITEMS:
            del BUFFER_ITEMS[nkey]
        if has_buffer_file(nkey):
            delete_buffer_file(nkey)


def buffer(version=1.0):
    '''
    Decorator to cache the result of a function.

    :param version: Cache version.
    '''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global BUFFER_ITEMS
            nkey = _get_hash_key(func.__name__, args, kwargs)
            if has_item_key(nkey):
                buffer_value = get_buffer_item(nkey)
                if buffer_value['version'] == version:
                    return buffer_value['value']

            func_result = func(*args, **kwargs)
            buffer_item(nkey, {'version': version, 'value': func_result})

            return func_result

        return wrapper

    return decorator
