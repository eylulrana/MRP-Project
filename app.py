# app.py
import streamlit as st
import pandas as pd
from db import run_query

def main():
    st.title("Geliştirilmiş MRP Sistemi - Streamlit Arayüz")

    menu = [
        "Ana Sayfa",
        "Plan Yönetimi",
        "Period Yönetimi",
        "Product Yönetimi",
        "BOM Yönetimi",
        "Demand/Inventory",
        "MRP Hesaplama",
        "Hakkında"
    ]
    choice = st.sidebar.selectbox("Menü", menu)

    # -----------------------------------------
    # 1) ANA SAYFA
    # -----------------------------------------
    if choice == "Ana Sayfa":
        st.write("Hoş geldiniz!")
        st.markdown("""
        Bu arayüz üzerinden MRP sistemi tablolarına veri girişi yapabilir, mevcut verileri görüntüleyebilir **ve hatta düzenleyebilirsiniz**.
        - **Plan Yönetimi**: Plan oluşturma / düzenleme
        - **Period Yönetimi**: Dönem ekleme / görüntüleme
        - **Product Yönetimi**: Ürün ekleme / düzenleme, lot size, stok vb.
        - **BOM Yönetimi**: Ürün ağacı tanımları
        - **Demand/Inventory**: Talep ve stok değerleri (Gross Req vb.)
        - **MRP Hesaplama**: Basit MRP sorgularını (Net Requirement, Planned Orders) tetikleyip sonuçları tablo olarak inceleme
        """)

    # -----------------------------------------
    # 2) PLAN YÖNETİMİ
    # -----------------------------------------
    elif choice == "Plan Yönetimi":
        st.subheader("Plan Tablosu Yönetimi")

        # Plan Ekleme
        with st.form("plan_form"):
            st.write("### Yeni Plan Ekle")
            plan_name = st.text_input("Plan Adı")
            start_date = st.text_input("Plan Başlangıç Tarihi (YYYY-MM-DD)")
            period_type = st.text_input("Period Tipi (Örn: 'Haftalık')")
            planning_horizon = st.number_input("Plan Horizon", min_value=1, value=12)
            submitted = st.form_submit_button("Kaydet")

        if submitted:
            if plan_name and start_date and period_type:
                insert_query = """
                INSERT INTO Plan (PlanName, StartDate, PeriodType, PlanningHorizon)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_name, start_date, period_type, planning_horizon))
                st.success(f"'{plan_name}' adlı plan eklendi.")
            else:
                st.warning("Lütfen tüm alanları doldurunuz.")

        # Mevcut Planlar
        st.write("### Mevcut Planlar")
        plan_rows = run_query("SELECT PlanID, PlanName, StartDate, PeriodType, PlanningHorizon FROM Plan;")
        df_plan = pd.DataFrame(plan_rows, columns=["PlanID", "PlanName", "StartDate", "PeriodType", "PlanningHorizon"])
        st.dataframe(df_plan)

        # Plan Güncelleme
        st.write("### Plan Güncelle")
        if len(df_plan) > 0:
            plan_ids = df_plan["PlanID"].tolist()
            selected_plan_id = st.selectbox("Güncellenecek Plan ID", plan_ids)
            if selected_plan_id:
                # Seçilen planın mevcut değerlerini al
                plan_data = run_query("SELECT PlanName, StartDate, PeriodType, PlanningHorizon FROM Plan WHERE PlanID=?", (selected_plan_id,))
                if plan_data:
                    current_name, current_start, current_type, current_horizon = plan_data[0]

                    new_name = st.text_input("Yeni Plan Adı", value=current_name)
                    new_start = st.text_input("Yeni Başlangıç Tarihi", value=current_start)
                    new_type = st.text_input("Yeni Period Tipi", value=current_type)
                    new_horizon = st.number_input("Yeni Horizon", min_value=1, value=current_horizon)

                    if st.button("Plan Güncelle"):
                        update_query = """
                        UPDATE Plan
                        SET PlanName = ?, StartDate = ?, PeriodType = ?, PlanningHorizon = ?
                        WHERE PlanID = ?
                        """
                        run_query(update_query, (new_name, new_start, new_type, new_horizon, selected_plan_id))
                        st.success("Plan başarıyla güncellendi.")
                        st.experimental_rerun()

    # -----------------------------------------
    # 3) PERIOD YÖNETİMİ
    # -----------------------------------------
    elif choice == "Period Yönetimi":
        st.subheader("Period Tablosu Yönetimi")

        # Plan ID'leri için selectbox
        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in plan_rows}

        with st.form("period_form"):
            st.write("### Yeni Period Ekle")
            selected_plan = st.selectbox("Hangi Plan?", list(plan_dict.keys()))
            period_seq = st.number_input("Period Sırası", min_value=1, value=1)
            start_date = st.text_input("Period Başlangıç Tarihi (YYYY-MM-DD)")
            end_date = st.text_input("Period Bitiş Tarihi (YYYY-MM-DD)")
            period_submitted = st.form_submit_button("Kaydet")

        if period_submitted:
            plan_id = plan_dict[selected_plan]
            if start_date and end_date:
                insert_query = """
                INSERT INTO Period (PlanID, PeriodSequence, StartDate, EndDate)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_id, period_seq, start_date, end_date))
                st.success("Period eklendi.")
            else:
                st.warning("Tarih alanlarını doldurunuz.")

        # Mevcut Periodlar
        st.write("### Mevcut Periodlar")
        rows = run_query("SELECT PeriodID, PlanID, PeriodSequence, StartDate, EndDate FROM Period;")
        df_period = pd.DataFrame(rows, columns=["PeriodID","PlanID","PeriodSequence","StartDate","EndDate"])
        st.dataframe(df_period)

        # Period Güncelleme (opsiyonel)
        st.write("### Period Güncelle")
        if len(df_period) > 0:
            period_ids = df_period["PeriodID"].tolist()
            sel_period_id = st.selectbox("Güncellenecek Period ID", period_ids)
            if sel_period_id:
                period_data = run_query(
                    "SELECT PlanID, PeriodSequence, StartDate, EndDate FROM Period WHERE PeriodID=?",
                    (sel_period_id,)
                )
                if period_data:
                    p_plan_id, p_seq, p_start, p_end = period_data[0]
                    # Plan adını göstermek için
                    plan_name_for_period = run_query("SELECT PlanName FROM Plan WHERE PlanID=?", (p_plan_id,))
                    plan_name_for_period = plan_name_for_period[0][0] if plan_name_for_period else f"PlanID:{p_plan_id}"
                    
                    new_seq = st.number_input("Yeni Sıra", min_value=1, value=p_seq)
                    new_start = st.text_input("Yeni Başlangıç Tarihi", value=p_start)
                    new_end = st.text_input("Yeni Bitiş Tarihi", value=p_end)

                    if st.button("Period Güncelle"):
                        update_period_query = """
                        UPDATE Period
                        SET PeriodSequence = ?, StartDate = ?, EndDate = ?
                        WHERE PeriodID = ?
                        """
                        run_query(update_period_query, (new_seq, new_start, new_end, sel_period_id))
                        st.success("Period güncellendi.")
                        st.experimental_rerun()

    # -----------------------------------------
    # 4) PRODUCT YÖNETİMİ
    # -----------------------------------------
    elif choice == "Product Yönetimi":
        st.subheader("Product Tablosu Yönetimi")

        # Yeni ürün ekleme
        with st.form("product_form"):
            st.write("### Yeni Ürün Ekle")
            product_name = st.text_input("Ürün Adı")
            product_type = st.text_input("Ürün Tipi", value="FinishedGood")
            lead_time = st.number_input("Lead Time", min_value=0, value=0)
            lot_size = st.number_input("Lot Size", min_value=1, value=1)
            on_hand = st.number_input("Mevcut Stok (OnHandInventory)", min_value=0, value=0)
            prod_submitted = st.form_submit_button("Kaydet")

        if prod_submitted:
            if product_name and product_type:
                insert_query = """
                INSERT INTO Product (ProductName, ProductType, LeadTime, LotSize, OnHandInventory)
                VALUES (?, ?, ?, ?, ?)
                """
                run_query(insert_query, (product_name, product_type, lead_time, lot_size, on_hand))
                st.success(f"{product_name} ürünü eklendi.")
            else:
                st.warning("Lütfen bütün alanları doldurun.")

        # Mevcut ürünleri göster
        st.write("### Mevcut Ürünler")
        rows = run_query("SELECT ProductID, ProductName, ProductType, LeadTime, LotSize, OnHandInventory FROM Product;")
        df_product = pd.DataFrame(rows, columns=["ProductID","ProductName","ProductType","LeadTime","LotSize","OnHand"])
        st.dataframe(df_product)

        # Ürün Güncelleme
        st.write("### Ürün Güncelle")
        if len(df_product) > 0:
            product_ids = df_product["ProductID"].tolist()
            sel_product_id = st.selectbox("Güncellenecek Ürün ID", product_ids)
            if sel_product_id:
                p_data = run_query("SELECT ProductName, ProductType, LeadTime, LotSize, OnHandInventory FROM Product WHERE ProductID=?", (sel_product_id,))
                if p_data:
                    cur_name, cur_type, cur_lead, cur_lot, cur_onhand = p_data[0]

                    new_name = st.text_input("Yeni Ürün Adı", value=cur_name)
                    new_type = st.text_input("Yeni Ürün Tipi", value=cur_type)
                    new_lead = st.number_input("Yeni Lead Time", min_value=0, value=cur_lead)
                    new_lot = st.number_input("Yeni Lot Size", min_value=1, value=cur_lot)
                    new_onhand = st.number_input("Yeni OnHandInventory", min_value=0, value=cur_onhand)

                    if st.button("Ürünü Güncelle"):
                        update_prod_query = """
                        UPDATE Product
                        SET ProductName=?, ProductType=?, LeadTime=?, LotSize=?, OnHandInventory=?
                        WHERE ProductID=?
                        """
                        run_query(update_prod_query, (new_name, new_type, new_lead, new_lot, new_onhand, sel_product_id))
                        st.success("Ürün güncellendi.")
                        st.experimental_rerun()

    # -----------------------------------------
    # 5) BOM YÖNETİMİ
    # -----------------------------------------
    elif choice == "BOM Yönetimi":
        st.subheader("BOM (Bill of Materials) Yönetimi")

        # Mevcut ürünleri al
        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        product_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in product_rows}

        with st.form("bom_form"):
            st.write("### Yeni BOM Kaydı Ekle")
            parent_selected = st.selectbox("Parent Ürün", list(product_dict.keys()))
            child_selected = st.selectbox("Child Ürün", list(product_dict.keys()))
            quantity = st.number_input("Gerekli Miktar (Quantity)", min_value=1.0, value=1.0)
            level = st.number_input("Seviye (Level)", min_value=0, value=1)
            bom_submitted = st.form_submit_button("Kaydet")

        if bom_submitted:
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
        st.write("### Mevcut BOM Kayıtları")
        rows = run_query("""
            SELECT b.BomID, p1.ProductName as Parent, p2.ProductName as Child, 
                   b.Quantity, b.Level
            FROM BOM b
            JOIN Product p1 ON b.ParentProductID = p1.ProductID
            JOIN Product p2 ON b.ChildProductID = p2.ProductID
        """)
        df_bom = pd.DataFrame(rows, columns=["BomID", "Parent", "Child", "Quantity", "Level"])
        st.dataframe(df_bom)

        # (İsteğe bağlı) BOM güncelleme / silme fonksiyonlarını da benzer şekilde ekleyebilirsiniz.

    # -----------------------------------------
    # 6) DEMAND/INVENTORY
    # -----------------------------------------
    elif choice == "Demand/Inventory":
        st.subheader("Demand / Inventory (Talep ve Stok Verileri)")

        # Plan/Period/Product seçimleri
        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in plan_rows}

        period_rows = run_query("SELECT PeriodID, StartDate, EndDate FROM Period;")
        period_dict = {f"Period {r[0]} ({r[1]} - {r[2]})": r[0] for r in period_rows}

        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        product_dict = {f"{r[1]} (ID:{r[0]})": r[0] for r in product_rows}

        with st.form("demandinventory_form"):
            st.write("### Yeni Talep/Stok Kaydı Ekle")
            selected_plan = st.selectbox("Plan Seçiniz", list(plan_dict.keys()))
            selected_period = st.selectbox("Period Seçiniz", list(period_dict.keys()))
            selected_product = st.selectbox("Ürün Seçiniz", list(product_dict.keys()))
            gross_req = st.number_input("Gross Requirements", min_value=0.0, value=0.0)
            scheduled_receipts = st.number_input("Scheduled Receipts", min_value=0.0, value=0.0)
            projected_inventory = st.number_input("Projected Inventory", min_value=0.0, value=0.0)
            net_req = st.number_input("Net Requirement", min_value=0.0, value=0.0)
            planned_order = st.number_input("Planned Order Releases", min_value=0.0, value=0.0)
            dem_submitted = st.form_submit_button("Kaydet")

        if dem_submitted:
            plan_id = plan_dict[selected_plan]
            period_id = period_dict[selected_period]
            product_id = product_dict[selected_product]

            insert_query = """
            INSERT INTO DemandInventory 
            (PlanID, PeriodID, ProductID,
             GrossRequirements, ScheduledReceipts, 
             ProjectedInventory, NetRequirement, PlannedOrderReleases)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            run_query(insert_query, (plan_id, period_id, product_id,
                                     gross_req, scheduled_receipts,
                                     projected_inventory, net_req, planned_order))
            st.success("Kayıt eklendi.")

        # Mevcut kayıtları göster
        st.write("### Mevcut DemandInventory Kayıtları")
        rows = run_query("""
            SELECT RecordID, PlanID, PeriodID, ProductID,
                   GrossRequirements, ScheduledReceipts,
                   ProjectedInventory, NetRequirement, PlannedOrderReleases
            FROM DemandInventory
        """)
        df_di = pd.DataFrame(rows, columns=[
            "RecordID", "PlanID", "PeriodID", "ProductID",
            "GrossReq", "ScheduledReceipts", "ProjInventory", "NetReq", "PlannedOrder"
        ])
        st.dataframe(df_di)

        # (İsteğe bağlı) Seçip güncelleme/silme mantığı eklenebilir.

    # -----------------------------------------
    # 7) MRP HESAPLAMA
    # -----------------------------------------
    elif choice == "MRP Hesaplama":
        st.subheader("MRP Hesaplaması")
        st.write("""
        Basit MRP hesaplamaları (Net Requirement = max(0, GrossReq - (ProjInventory + SchedReceipts))
        ve PlannedOrder = NetRequirement [lot-for-lot]) şeklinde güncellenebilir.
        """)

        if st.button("MRP Sorgularını Çalıştır"):
            # NetRequirement hesapla
            update_query_netreq = """
            UPDATE DemandInventory
            SET NetRequirement = CASE
                WHEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts)) > 0
                THEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts))
                ELSE 0
            END
            """
            run_query(update_query_netreq)

            # PlannedOrderReleases = NetRequirement
            update_query_planned = """
            UPDATE DemandInventory
            SET PlannedOrderReleases = NetRequirement
            """
            run_query(update_query_planned)

            st.success("MRP hesaplamaları tamamlandı.")

        # Sonuçları göster
        rows = run_query("""
            SELECT RecordID, PlanID, PeriodID, ProductID,
                   GrossRequirements, ScheduledReceipts,
                   ProjectedInventory, NetRequirement, PlannedOrderReleases
            FROM DemandInventory
            ORDER BY RecordID
        """)
        df_res = pd.DataFrame(rows, columns=[
            "RecordID","PlanID","PeriodID","ProductID",
            "GrossReq","ScheduledReceipts","ProjInventory","NetReq","PlannedOrder"
        ])
        st.dataframe(df_res)

    # -----------------------------------------
    # 8) HAKKINDA
    # -----------------------------------------
    else:
        st.subheader("Hakkında")
        st.write("""
        **Bu proje**, IE 442 dersi kapsamında geliştirilen basit bir MRP (Material Requirements Planning)
        uygulamasıdır. Streamlit kullanarak veritabanını (SQLite) hem yönetiyor hem de 
        hesaplamaları tetikleyebiliyoruz.
        
        ### Temel Özellikler
        - Plan, Period, Product, BOM tabloları
        - Demand/Inventory tablolarında Gross Req, Net Req, vb. sütunlar
        - Basit MRP hesaplaması (lot-for-lot)
        - Streamlit formlarıyla ekleme / güncelleme
        """)

if __name__ == "__main__":
    main()
