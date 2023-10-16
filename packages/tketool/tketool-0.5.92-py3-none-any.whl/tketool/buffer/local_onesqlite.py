import os
import sqlite3
import json
from tketool.JConfig import get_config_instance
import tketool.buffer.bufferbase as bb

# Global variables should be in uppercase according to PEP8
BUFFER_FOLDER = get_config_instance().get_config("buffer_folder", "buffer")
BUFFER_FILE_PATH = os.path.join(os.getcwd(), BUFFER_FOLDER, "buffer.db")


def init_db():
    """
    Initializes the SQLite database and updates the bufferbase module.
    """
    if not os.path.exists(BUFFER_FOLDER):
        os.makedirs(BUFFER_FOLDER)

    conn = sqlite3.connect(BUFFER_FILE_PATH)
    c = conn.cursor()

    # create table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS buffer (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    ''')
    conn.commit()

    def _load_buffer_file(key):
        c.execute("SELECT value FROM buffer WHERE key = ?", (key,))
        row = c.fetchone()
        if row is not None:
            return json.loads(row[0])
        else:
            return None

    def _save_buffer_file(lists):
        for k, v in lists:
            c.execute("REPLACE INTO buffer (key, value) VALUES (?, ?)", (k, json.dumps(v)))
        conn.commit()

    def _delete_buffer_file(key):
        c.execute("DELETE FROM buffer WHERE key = ?", (key,))
        conn.commit()

    def _has_buffer_file(key):
        c.execute("SELECT 1 FROM buffer WHERE key = ?", (key,))
        row = c.fetchone()
        return row is not None

    bb.has_buffer_file = _has_buffer_file
    bb.load_buffer_file = _load_buffer_file
    bb.delete_buffer_file = _delete_buffer_file
    bb.save_buffer_file = _save_buffer_file

    return conn, c


# Initialize the SQLite connection and cursor and store them in global variables
CONN_OBJ, CURSOR_OBJ = init_db()


def close_db():
    """
    Closes the SQLite connection.
    """
    global CONN_OBJ
    if CONN_OBJ:
        CONN_OBJ.close()
        CONN_OBJ = None
