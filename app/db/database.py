import sqlite3
import os

"""
Search History Database

Initializes and manages the SQLite database used to store search history.
Provides a helper for creating database connections and a function to
initialize the required table.

The database stores:
- filename of the searched document
- user question
- extracted answer
- confidence score
- timestamp of the request
"""

DB_PATH = "data/history.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            question TEXT NOT NULL,
            answer TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
