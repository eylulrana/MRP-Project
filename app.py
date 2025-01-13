import streamlit as st
import pandas as pd
import sqlite3
from db import DB_NAME, run_query, get_connection

def create_tables_if_not_exists():
    """
    Opsiyonel: Uygulama her açıldığında tablolar yoksa oluştursun diye.
    Ama normalde main.py'de zaten yapıyorsanız tekrarlamanıza gerek yok.
    """
    # Burada isterseniz main.py'deki create_tables.sql'i tekrar çalıştırabilirsiniz.
    pass

def show_productperiod_data():
    """
    ProductPeriod (veya DemandInventory) tablosundaki MRP sonuçlarını bir tablo halinde gösterir.
    """
    # Basitçe tabloyu çeken bir SELECT sorgusu:
    query = """
    SELECT ProductID, PeriodID, PlanID, 
           GrossRequirements, ScheduledReceipts, 
           NetRequirement, PlannedOrderReleases
    FROM ProductPeriod
    """
    rows = run_query(query)
    df = pd.DataFrame(rows, columns=[
        "ProductID", "PeriodID", "PlanID", 
        "GrossReq", "ScheduledReceipts", 
        "NetReq", "PlannedOrderReleases"
    ])
    st.dataframe(df)

def main():
    st.title("Basit MRP Uygulaması")

    # Kenar çubuğu veya üst menü
    menu = ["Ana Sayfa", "MRP Sonuçları", "Hakkında"]
    choice = st.sidebar.selectbox("Menü", menu)

    if choice == "Ana Sayfa":
        st.write("Hoş geldiniz! Bu basit Streamlit arayüzü ile MRP sonuçlarını görüntüleyebilirsiniz.")
        if st.button("Veritabanını Kur / Güncelle"):
            # main.py'deki kodu ya da create_tables.sql'i burada tekrar çalıştırabilirsiniz (opsiyonel).
            st.success("Veritabanı tabloları ve veriler yüklendi (opsiyonel).")

    elif choice == "MRP Sonuçları":
        st.subheader("MRP Sonuç Tablosu")
        show_productperiod_data()

    else:  # "Hakkında"
        st.subheader("Hakkında")
        st.write("Bu proje, IE 442 dersi kapsamında hazırlanmış basit bir MRP uygulamasıdır.")
        st.write("Streamlit kullanarak veritabanındaki sonuçları gösteriyoruz.")

if __name__ == "__main__":
    main()
