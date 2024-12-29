"""Intialize SQLite Database"""

import os
from pathlib import Path
from sqlite3 import connect, Cursor, Connection, IntegrityError
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
conn: Optional[Connection] = None
cur: Optional[Cursor] = None


def get_db(name: Optional[str] = None, reset: bool = False):
    global conn, cur
    if conn:
        if not reset:
            return
        conn = None

    if not name == ":memory:":
        top_dir = Path(__file__).resolve().parents[1]
        db_dir = top_dir / "db"
        db_path = os.path.join(db_dir, name)
        # Default behavior (check_same_thread=True): By default, check_same_thread is set to True.
        # This means that SQLite will raise an exception if a thread tries to use a database connection
        # created in a different thread. This is a safety feature to prevent concurrency issues
        # because SQLite connections are not thread-safe.

        # When check_same_thread=False: Setting check_same_thread=False disables this check.
        # It allows the database connection to be shared across multiple threads.
        # This is useful if you have a multi-threaded application and you want to share the
        # same connection between threads. However, it's your responsibility to ensure thread safety
        # by using appropriate locking mechanisms (e.g., a threading.Lock) to avoid race conditions or
        # data corruption
        conn = connect(db_path, check_same_thread=False)
        cur = conn.cursor()
    conn = connect(name, check_same_thread=True)
    cur = conn.cursor()


get_db(os.getenv("MYSTICAL_SQLITE_DB"))
