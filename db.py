# db.py
import sqlite3
import os

DB_NAME = "my_mrp.db"

def get_connection():
    """
    Veritabanı bağlantısını döndürür. 
    Foreign key kısıtlamalarının aktif olması için 'PRAGMA foreign_keys = ON;' ekliyoruz.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_script_from_file(filepath):
    """
    Bir .sql dosyasını okuyup içerisindeki tüm komutları çalıştırır.
    """
    conn = get_connection()
    with open(filepath, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

def run_query(query, params=None):
    """
    Tek seferlik bir SELECT veya UPDATE sorgusu çalıştırır.
    """
    if params is None:
        params = ()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()  # SELECT ise sonuçlar
    conn.commit()
    conn.close()
    return rows
