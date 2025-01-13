# db.py
import sqlite3
import os

DB_NAME = "mrp.db"

def get_connection():
    """
    Returns a connection to the SQLite database.
    Enables foreign key constraints.
    """
    # Veritabanı dosyasını proje klasöründe oluştur
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def reset_database():
    """Veritabanını sıfırla ve yeniden oluştur"""
    try:
        # Veritabanını sil
        db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Tabloları oluştur
        execute_script_from_file("sql/create_tables.sql")
        
        # Test verilerini ekle
        execute_script_from_file("sql/insert_test_data.sql")
        return True
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False

def run_query(sql, params=()):
    """
    Executes a single SQL query (SELECT, INSERT, UPDATE, etc.) 
    with optional parameters. Returns all fetched rows (if any).
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        rows = cur.fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()

def execute_script_from_file(filepath):
    """SQL dosyasından script çalıştırma"""
    # Tam dosya yolunu oluştur
    full_path = os.path.join(os.path.dirname(__file__), filepath)
    
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"SQL file not found: {full_path}")
        
    conn = get_connection()
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            script = f.read()
        conn.executescript(script)
        conn.commit()
    except Exception as e:
        print(f"Error executing SQL script: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
