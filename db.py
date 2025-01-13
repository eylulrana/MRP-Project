# db.py
import sqlite3

DB_NAME = "mrp.db"  # veya sizin veritabanı dosyanız

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def run_query(sql, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def execute_script_from_file(filepath):
    conn = get_connection()
    with open(filepath, 'r', encoding='utf-8') as f:
        script = f.read()
    conn.executescript(script)
    conn.commit()
    conn.close()
