import shelve
from tketool.JConfig import *

shelve_obj = None


def _load():
    global shelve_obj
    if shelve_obj is None:
        path = get_config_instance().get_config("state_file_path", "state.shelve")
        shelve_obj = shelve.open(path)
    return shelve_obj


def set_value(key, v):
    obj = _load()
    obj[key] = v


def get_value(key):
    obj = _load()
    if key in obj:
        return obj[key]
    else:
        return None


def has_value(key):
    obj = _load()
    return key in obj


def value_add(key, v):
    obj = _load()
    if key not in obj:
        obj[key] = 0
    obj[key] = obj[key] + v
    return obj[key]
