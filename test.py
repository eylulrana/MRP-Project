# test_mrp.py
import unittest
from db import run_query, execute_script_from_file

class TestMRP(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Tabloları sıfırdan oluşturup verileri ekle
        execute_script_from_file("sql/create_tables.sql")
        execute_script_from_file("sql/insert_test_data.sql")
        execute_script_from_file("sql/mrp_queries.sql")

    def test_net_requirement(self):
        # Basit bir test: NetRequirement pozitif mi?
        rows = run_query("SELECT NetRequirement FROM ProductPeriod WHERE ProductID=100 AND PeriodID=1 AND PlanID=1;")
        # Örnek olarak, beklediğimiz net requirement 0 veya üstü
        self.assertTrue(rows[0][0] >= 0)
    
    def test_planned_order_releases(self):
        # Diğer testler...
        rows = run_query("SELECT PlannedOrderReleases FROM ProductPeriod WHERE ProductID=100 AND PeriodID=2 AND PlanID=1;")
        self.assertTrue(rows[0][0] >= 0)

if __name__ == '__main__':
    unittest.main()

"""
import sqlite3

def check_data():
    conn = sqlite3.connect("mrp.db")
    cur = conn.cursor()

    # Örneğin, Plan tablosundaki verileri görelim
    cur.execute("SELECT * FROM Plan;")
    plans = cur.fetchall()
    print("Plans:", plans)

    # Period tablosundaki verileri görelim
    cur.execute("SELECT * FROM Period;")
    periods = cur.fetchall()
    print("Periods:", periods)

    # Product tablosundaki verileri görelim
    cur.execute("SELECT * FROM Product;")
    products = cur.fetchall()
    print("Products:", products)

    # DemandInventory tablosundaki veriler
    cur.execute("SELECT * FROM DemandInventory;")
    demand_inventory = cur.fetchall()
    print("Demand & Inventory:", demand_inventory)

    conn.close()

if __name__ == "__main__":
    check_data()
"""