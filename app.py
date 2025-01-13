# app.py
import streamlit as st
import pandas as pd
from db import run_query

def main():
    st.title("Basit MRP Sistemi - Streamlit Arayüz")

    menu = [
        "Ana Sayfa",
        "Plan Yönetimi",
        "Period Yönetimi",
        "Product Yönetimi",
        "BOM Yönetimi",
        "Demand/Inventory",
        "MRP Hesapla",
        "Hakkında"
    ]
    choice = st.sidebar.selectbox("Menü", menu)

    if choice == "Ana Sayfa":
        st.write("Hoş geldiniz!")
        st.markdown("""
        Bu arayüz üzerinden MRP sistemi tablolarına veri girişi yapabilir ve mevcut verileri görüntüleyebilirsiniz.
        Ayrıca 'MRP Hesapla' sekmesi ile basit MRP sorgularını çalıştırıp sonuçları görebilirsiniz.
        """)

    elif choice == "Plan Yönetimi":
        st.subheader("Plan Tablosu Yönetimi")
        
        # Veri Ekleme Formu
        with st.form("plan_form"):
            plan_name = st.text_input("Plan Adı")
            start_date = st.text_input("Plan Başlangıç Tarihi (YYYY-MM-DD)")
            period_type = st.text_input("Period Tipi (örn: 'Haftalık', 'Aylık')")
            planning_horizon = st.number_input("Plan Horizon (örn: 12)", min_value=1, value=12)
            submitted = st.form_submit_button("Kaydet")
        
        if submitted:
            if plan_name and start_date and period_type:
                insert_query = """
                INSERT INTO Plan(PlanName, StartDate, PeriodType, PlanningHorizon)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_name, start_date, period_type, planning_horizon))
                st.success(f"{plan_name} planı eklendi.")
            else:
                st.warning("Lütfen tüm alanları doldurunuz.")

        # Mevcut Planları Göster
        rows = run_query("SELECT PlanID, PlanName, StartDate, PeriodType, PlanningHorizon FROM Plan;")
        df = pd.DataFrame(rows, columns=["PlanID", "PlanName", "StartDate", "PeriodType", "PlanningHorizon"])
        st.dataframe(df)

    elif choice == "Period Yönetimi":
        st.subheader("Period Tablosu Yönetimi")
        
        # Plan ID'leri çekip seçim yaptırmak isterseniz:
        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in plan_rows}
        
        with st.form("period_form"):
            selected_plan = st.selectbox("Hangi Plan?", list(plan_dict.keys()))
            period_sequence = st.number_input("Period Sırası (örn: 1)", min_value=1, value=1)
            start_date = st.text_input("Başlangıç Tarihi (YYYY-MM-DD)")
            end_date = st.text_input("Bitiş Tarihi (YYYY-MM-DD)")
            submitted = st.form_submit_button("Kaydet")

        if submitted:
            plan_id = plan_dict[selected_plan]
            if start_date and end_date:
                insert_query = """
                INSERT INTO Period (PlanID, PeriodSequence, StartDate, EndDate)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_id, period_sequence, start_date, end_date))
                st.success(f"Period eklendi. PlanID: {plan_id}, Sıra: {period_sequence}")
            else:
                st.warning("Lütfen tüm tarih alanlarını doldurunuz.")

        # Mevcut Period'ları göster
        rows = run_query("SELECT PeriodID, PlanID, PeriodSequence, StartDate, EndDate FROM Period;")
        df = pd.DataFrame(rows, columns=["PeriodID", "PlanID", "PeriodSequence", "StartDate", "EndDate"])
        st.dataframe(df)

    elif choice == "Product Yönetimi":
        st.subheader("Product Tablosu Yönetimi")
        
        # Ürün ekleme
        with st.form("product_form"):
            product_name = st.text_input("Ürün Adı")
            product_type = st.text_input("Ürün Tipi (örn: 'FinishedGood', 'RawMaterial')")
            lead_time = st.number_input("Lead Time (gün/hafta)", min_value=0, value=0)
            on_hand = st.number_input("Mevcut Stok", min_value=0, value=0)
            submitted = st.form_submit_button("Kaydet")

        if submitted:
            if product_name and product_type:
                insert_query = """
                INSERT INTO Product (ProductName, ProductType, LeadTime, OnHandInventory)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (product_name, product_type, lead_time, on_hand))
                st.success(f"{product_name} ürünü eklendi.")
            else:
                st.warning("Lütfen bütün alanları doldurun.")
        
        # Mevcut ürünleri göster
        rows = run_query("SELECT ProductID, ProductName, ProductType, LeadTime, OnHandInventory FROM Product;")
        df = pd.DataFrame(rows, columns=["ProductID", "ProductName", "ProductType", "LeadTime", "OnHandInventory"])
        st.dataframe(df)

    elif choice == "BOM Yönetimi":
        st.subheader("BOM (Bill of Materials) Yönetimi")

        # Mevcut ürünleri çekelim
        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        product_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in product_rows}

        with st.form("bom_form"):
            parent_selected = st.selectbox("Parent Ürün Seçiniz", list(product_dict.keys()))
            child_selected = st.selectbox("Child Ürün Seçiniz", list(product_dict.keys()))
            quantity = st.number_input("Gerekli Miktar", min_value=1, value=1)
            level = st.number_input("Seviye (Level)", min_value=0, value=1)
            submitted = st.form_submit_button("Kaydet")

        if submitted:
            parent_id = product_dict[parent_selected]
            child_id = product_dict[child_selected]
            if parent_id == child_id:
                st.error("Parent ve Child ürün aynı olamaz.")
            else:
                insert_query = """
                INSERT INTO BOM (ParentProductID, ChildProductID, Quantity, Level)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (parent_id, child_id, quantity, level))
                st.success("BOM kaydı eklendi.")

        # Mevcut BOM kayıtlarını göster
        rows = run_query("""
            SELECT b.BomID, p1.ProductName as Parent, p2.ProductName as Child, 
                   b.Quantity, b.Level
            FROM BOM b
            JOIN Product p1 ON b.ParentProductID = p1.ProductID
            JOIN Product p2 ON b.ChildProductID = p2.ProductID
        """)
        df = pd.DataFrame(rows, columns=["BomID", "Parent", "Child", "Quantity", "Level"])
        st.dataframe(df)

    elif choice == "Demand/Inventory":
        st.subheader("Demand / Inventory (Talep ve Stok Değerleri)")
        st.markdown("""
        Bu tabloda (DemandInventory veya ProductPeriod gibi) brüt talep, planlanan alım vb. değerleri saklayabilirsiniz.
        """)

        # Plan/Period/Product seçimleri
        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in plan_rows}
        
        period_rows = run_query("SELECT PeriodID, StartDate, EndDate FROM Period;")
        period_dict = {f"Period {r[0]} ({r[1]} - {r[2]})": r[0] for r in period_rows}

        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        product_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in product_rows}

        with st.form("demandinventory_form"):
            selected_plan = st.selectbox("Plan Seçiniz", list(plan_dict.keys()))
            selected_period = st.selectbox("Period Seçiniz", list(period_dict.keys()))
            selected_product = st.selectbox("Ürün Seçiniz", list(product_dict.keys()))
            gross_req = st.number_input("Gross Requirements", min_value=0, value=0)
            scheduled_receipts = st.number_input("Scheduled Receipts", min_value=0, value=0)
            projected_inventory = st.number_input("Projected Inventory", min_value=0, value=0)
            net_req = st.number_input("Net Requirement", min_value=0, value=0)
            planned_order = st.number_input("Planned Order Releases", min_value=0, value=0)
            submitted = st.form_submit_button("Kaydet")

        if submitted:
            plan_id = plan_dict[selected_plan]
            period_id = period_dict[selected_period]
            product_id = product_dict[selected_product]
            query = """
            INSERT INTO DemandInventory 
            (PlanID, PeriodID, ProductID, 
             GrossRequirements, ScheduledReceipts, 
             ProjectedInventory, NetRequirement, PlannedOrderReleases)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            run_query(query, (plan_id, period_id, product_id,
                              gross_req, scheduled_receipts, 
                              projected_inventory, net_req, planned_order))
            st.success("Kayıt eklendi.")

        # Mevcut kayıtları göster
        rows = run_query("""
            SELECT RecordID, PlanID, PeriodID, ProductID,
                   GrossRequirements, ScheduledReceipts,
                   ProjectedInventory, NetRequirement, PlannedOrderReleases
            FROM DemandInventory
        """)
        df = pd.DataFrame(rows, columns=[
            "RecordID","PlanID","PeriodID","ProductID",
            "GrossReq","SchedReceipts","ProjInventory","NetReq","PlannedOrder"
        ])
        st.dataframe(df)

    elif choice == "MRP Hesapla":
        st.subheader("MRP Hesaplama")
        st.write("Bu bölümde, basit MRP sorgularını tetikleyebilirsiniz. (Örn. Net Req = Gross Req - (Projected + Sched) vs.)")

        if st.button("Hesaplama Sorgularını Çalıştır"):
            # Örnek basit sorgu: NetRequirement hesapla
            update_query_netreq = """
            UPDATE DemandInventory
            SET NetRequirement = CASE
                WHEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts)) > 0
                     THEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts))
                ELSE 0
            END
            """
            run_query(update_query_netreq)

            # PlannedOrderReleases = NetRequirement (lot-for-lot varsayım)
            update_query_planned = """
            UPDATE DemandInventory
            SET PlannedOrderReleases = NetRequirement
            """
            run_query(update_query_planned)

            st.success("MRP basit hesaplamalar tamamlandı.")

        # Sonuçları göster
        rows = run_query("""
            SELECT RecordID, PlanID, PeriodID, ProductID,
                   GrossRequirements, ScheduledReceipts,
                   ProjectedInventory, NetRequirement, PlannedOrderReleases
            FROM DemandInventory
        """)
        df = pd.DataFrame(rows, columns=[
            "RecordID","PlanID","PeriodID","ProductID",
            "GrossReq","SchedReceipts","ProjInventory","NetReq","PlannedOrder"
        ])
        st.dataframe(df)

    else:  # "Hakkında"
        st.subheader("Hakkında")
        st.write("""
        Bu proje, IE 442 dersi kapsamındaki temel bir MRP sisteminin Streamlit arayüzüyle yönetilmesi örneğidir.
        - **Plan Yönetimi**: Yeni plan ekleyebilir, var olan planları görebilirsiniz.
        - **Period Yönetimi**: Her planın dönemlerini ekler/inceleyebilirsiniz.
        - **Product Yönetimi**: Ürün/ham madde tanımları.
        - **BOM Yönetimi**: Ürün ağacı (Parent-Child) tanımları.
        - **Demand/Inventory**: Brüt talep, stok, planlanan sipariş gibi verileri tutar.
        - **MRP Hesapla**: Basit MRP algoritması (lot-for-lot) ile net ihtiyaç vb. değerleri günceller.
        """)

if __name__ == "__main__":
    main()
