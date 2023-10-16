import shelve
import os
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb

# Global variables should be in uppercase according to PEP8
BUFFER_FOLDER = get_config_instance().get_config("buffer_folder", "buffer")
BUFFER_FILE_PATH = os.path.join(os.getcwd(), BUFFER_FOLDER, "buffer.bin")


def init_shelve():
    """
    Initializes the shelve object and updates the bufferbase module.
    """
    if not os.path.exists(BUFFER_FOLDER):
        os.makedirs(BUFFER_FOLDER)

    shelve_obj = shelve.open(BUFFER_FILE_PATH)

    def _load_buffer_file(key):
        return shelve_obj.get(key)

    def _save_buffer_file(lists):
        for k, v in lists:
            shelve_obj[k] = v
        shelve_obj.sync()

    def _delete_buffer_file(key):
        del shelve_obj[key]
        shelve_obj.sync()

    def _has_buffer_file(key):
        lllm = [kk for kk in shelve_obj.keys()]
        return key in shelve_obj

    bb.has_buffer_file = _has_buffer_file
    bb.load_buffer_file = _load_buffer_file
    bb.delete_buffer_file = _delete_buffer_file
    bb.save_buffer_file = _save_buffer_file

    return shelve_obj


# Initialize the shelve object and store it in a global variable
SHELVE_OBJ = init_shelve()


def close_shelve():
    """
    Closes the shelve object.
    """
    global SHELVE_OBJ
    if SHELVE_OBJ:
        SHELVE_OBJ.close()
        SHELVE_OBJ = None
