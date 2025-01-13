# db.py
import sqlite3

DB_NAME = "mrp.db"

def get_connection():
    """
    Returns a connection to the SQLite database.
    Enables foreign key constraints.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def run_query(sql, params=()):
    """
    Executes a single SQL query (SELECT, INSERT, UPDATE, etc.) 
    with optional parameters. Returns all fetched rows (if any).
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def execute_script_from_file(filepath):
    """
    Reads and executes all SQL statements from a file 
    (e.g., create_tables.sql). Useful for initial setup.
    """
    conn = get_connection()
    with open(filepath, 'r', encoding='utf-8') as f:
        script = f.read()
    conn.executescript(script)
    conn.commit()
    conn.close()
