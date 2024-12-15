import sqlite3

def run_sql_script(db_name, script_file):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    with open(script_file, 'r') as f:
        sql_script = f.read()
    cur.executescript(sql_script)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Veritabanı ve tabloları oluştur
    run_sql_script("mrp.db", "schema.sql")
    print("Schema created successfully.")

    # Test verilerini ekle
    run_sql_script("mrp.db", "test_data.sql")
    print("Test data inserted successfully.")
