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
