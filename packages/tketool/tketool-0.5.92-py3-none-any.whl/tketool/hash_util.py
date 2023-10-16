
from collections.abc import Iterable
import hashlib


def hash_str(target_str: str) -> str:
    """
    Hash a string using MD5.

    :param target_str: String to be hashed.
    :return: Hashed string.
    """
    if not isinstance(target_str, str):
        target_str = str(target_str)

    return hashlib.md5(target_str.encode("utf8")).hexdigest()


def hash_obj_strbase(obj) -> str:
    """
    Recursively hash an object based on its string representation.

    :param obj: Object to be hashed.
    :return: Hash value.
    """
    if isinstance(obj, (str, int, float)):
        return hash_str(str(obj))

    if isinstance(obj, dict):
        keys_hashed = hash_obj_strbase(list(obj.keys()))
        values_hashed = hash_obj_strbase(list(obj.values()))
        return hash_str(keys_hashed + values_hashed)

    if isinstance(obj, Iterable):
        items_hashed_list = [hash_obj_strbase(x) for x in obj]
        return hash_str("".join(items_hashed_list))

    return hash_str(str(obj.__class__))
