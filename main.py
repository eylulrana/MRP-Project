# main.py
import os
from db import execute_script_from_file, run_query

def main():
    # 1) Veritabanı tablolarını oluştur (create_tables.sql)
    print("[INFO] Creating tables...")
    execute_script_from_file("sql/create_tables.sql")
    
    # 2) Örnek veri ekle (insert_sample_data.sql)
    print("[INFO] Inserting sample data...")
    execute_script_from_file("sql/insert_test_data.sql")
    
    # 3) MRP hesap sorgularını çalıştır (mrp_queries.sql)
    print("[INFO] Running MRP queries...")
    execute_script_from_file("sql/mrp_queries.sql")

    # 4) Sonuçları incelemek için basit bir SELECT
    print("[INFO] Checking results from ProductPeriod table:")
    rows = run_query("SELECT ProductID, PeriodID, PlanID, GrossRequirements, ScheduledReceipts, NetRequirement, PlannedOrderReleases FROM ProductPeriod;")
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()

"""
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
"""