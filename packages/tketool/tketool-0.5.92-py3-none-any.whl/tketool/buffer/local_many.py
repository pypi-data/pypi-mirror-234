
import pickle
import os
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb
from tketool.buffer.bufferbase import buffer


def get_path_for_key(key: str) -> str:
    """
    Generates the full path for a given key.
    """
    buffer_folder = get_config_instance().get_config("buffer_folder", "buffer")
    return os.path.join(buffer_folder, key)


def _load_buffer_file(key):
    """
    Load an item from the buffer file based on the key.
    """
    path = get_path_for_key(key)
    with open(path, 'rb') as f:
        return pickle.load(f)


def _save_buffer_file(lists):
    """
    Save a list of items to buffer files.
    """
    folder = os.path.dirname(get_path_for_key(""))
    if not os.path.exists(folder):
        os.makedirs(folder)  # Ensure all necessary directories are created

    for key, item in lists:
        path = get_path_for_key(key)
        with open(path, 'wb') as f:
            pickle.dump(item, f)


def _delete_buffer_file(key):
    """
    Delete a buffer file based on the key.
    """
    path = get_path_for_key(key)
    if os.path.exists(path):
        os.remove(path)


def _has_buffer_file(key):
    """
    Check if a buffer file exists for the given key.
    """
    return os.path.exists(get_path_for_key(key))


# Update bufferbase with the implemented functions
bb.has_buffer_file = _has_buffer_file
bb.load_buffer_file = _load_buffer_file
bb.delete_buffer_file = _delete_buffer_file
bb.save_buffer_file = _save_buffer_file
