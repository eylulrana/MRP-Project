# app.py
import streamlit as st
import pandas as pd
from db import run_query, execute_script_from_file

st.set_page_config(page_title="MRP Project")

def init_db_if_needed():
    """
    Checks if the 'Product' table exists. If it doesn't,
    we assume the database is empty and execute create_tables.sql.
    This is helpful in ephemeral environments like Streamlit Cloud.
    """
    check = run_query("SELECT name FROM sqlite_master WHERE type='table' AND name='Product';")
    if len(check) == 0:
        # Tables not found, create them from the script
        execute_script_from_file("sql/create_tables.sql")
        st.info("Database tables have been created.")

def show_existing_tables():
    """
    Fetch and display a list of all existing tables 
    EXCEPT the 'Product' table if you wish to hide it entirely.
    You could comment this entire function out if you want nothing 
    to appear on the home page regarding existing tables.
    """
    st.markdown("#### Existing Tables and Their Data")
    tables = run_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
    if tables:
        for t in tables:
            table_name = t[0]
            # If you want to skip showing 'Product' table completely:
            # if table_name == 'Product':
            #     continue
            st.subheader(f"Table: {table_name}")
            col_info = run_query(f"PRAGMA table_info({table_name});")
            col_names = [c[1] for c in col_info]
            data = run_query(f"SELECT * FROM {table_name}")
            if data:
                df = pd.DataFrame(data, columns=col_names)
                st.dataframe(df)
            else:
                st.write("No data in this table.")
    else:
        st.write("No tables found in the database.")

def main():
    st.title("MRP Project")
    st.markdown("### *Eylül Rana Öztekin*")
    st.markdown("## *2019402126*")

    # Ensure DB is initialized
    init_db_if_needed()

    menu = [
        "Home",
        "Plan Management",
        "Period Management",
        "Product Management",
        "BOM Management",
        "Demand/Inventory",
        "MRP Calculation",
        "About"
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    # -------------------------------------------------------------------
    # HOME PAGE
    # -------------------------------------------------------------------
    if choice == "Home":
        st.write("Welcome to the MRP System!")
        st.markdown("""
        This interface allows you to manage and explore the database
        for a simple Material Requirements Planning (MRP) application.
        
        - **Plan Management**: Create or update Plans.
        - **Period Management**: Manage time Periods for each Plan.
        - **Product Management**: Create new Products (we removed displaying existing products).
        - **BOM Management**: Define Bill of Materials relationships (Parent-Child).
        - **Demand/Inventory**: Manage demand and stock data (Gross Requirements, Net Requirement, etc.).
        - **MRP Calculation**: Perform simple MRP logic (lot-for-lot).
        
        Below, you can see some existing tables and any data they contain.
        """)
        # Show existing tables (if you want to hide Product table data, see the function above).
        show_existing_tables()

    # -------------------------------------------------------------------
    # PLAN MANAGEMENT
    # -------------------------------------------------------------------
    elif choice == "Plan Management":
        st.subheader("Plan Management")

        # Form to add a new plan
        with st.form("plan_form"):
            st.write("### Add a New Plan")
            plan_name = st.text_input("Plan Name")
            start_date = st.text_input("Start Date (YYYY-MM-DD)")
            period_type = st.text_input("Period Type (e.g. 'Weekly')")
            planning_horizon = st.number_input("Planning Horizon", min_value=1, value=12)
            submitted = st.form_submit_button("Add Plan")

        if submitted:
            if plan_name and start_date and period_type:
                insert_query = """
                INSERT INTO Plan (PlanName, StartDate, PeriodType, PlanningHorizon)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_name, start_date, period_type, planning_horizon))
                st.success(f"Plan '{plan_name}' has been added.")
            else:
                st.warning("Please fill in all fields.")

        # Display existing Plans
        st.write("### Existing Plans")
        plan_rows = run_query("SELECT PlanID, PlanName, StartDate, PeriodType, PlanningHorizon FROM Plan;")
        df_plan = pd.DataFrame(plan_rows, columns=["PlanID", "PlanName", "StartDate", "PeriodType", "Horizon"])
        st.dataframe(df_plan)

        # Update an existing Plan
        st.write("### Update a Plan")
        if not df_plan.empty:
            plan_ids = df_plan["PlanID"].tolist()
            selected_plan_id = st.selectbox("Select Plan ID to Update", plan_ids)
            if selected_plan_id:
                current = run_query(
                    "SELECT PlanName, StartDate, PeriodType, PlanningHorizon FROM Plan WHERE PlanID=?",
                    (selected_plan_id,)
                )
                if current:
                    cur_name, cur_start, cur_type, cur_horizon = current[0]
                    new_name = st.text_input("New Plan Name", value=cur_name)
                    new_start = st.text_input("New Start Date", value=cur_start)
                    new_type = st.text_input("New Period Type", value=cur_type)
                    new_horizon = st.number_input("New Planning Horizon", min_value=1, value=cur_horizon)

                    if st.button("Update Plan"):
                        update_query = """
                        UPDATE Plan
                        SET PlanName=?, StartDate=?, PeriodType=?, PlanningHorizon=?
                        WHERE PlanID=?
                        """
                        run_query(update_query, (new_name, new_start, new_type, new_horizon, selected_plan_id))
                        st.success("Plan updated successfully.")
                        st.experimental_rerun()

    # -------------------------------------------------------------------
    # PERIOD MANAGEMENT
    # -------------------------------------------------------------------
    elif choice == "Period Management":
        st.subheader("Period Management")

        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in plan_rows}

        with st.form("period_form"):
            st.write("### Add a New Period")
            selected_plan = st.selectbox("Select Plan", list(plan_dict.keys()))
            period_seq = st.number_input("Period Sequence", min_value=1, value=1)
            start_date = st.text_input("Start Date (YYYY-MM-DD)")
            end_date = st.text_input("End Date (YYYY-MM-DD)")
            submitted = st.form_submit_button("Add Period")

        if submitted:
            plan_id = plan_dict[selected_plan]
            if start_date and end_date:
                insert_query = """
                INSERT INTO Period (PlanID, PeriodSequence, StartDate, EndDate)
                VALUES (?, ?, ?, ?)
                """
                run_query(insert_query, (plan_id, period_seq, start_date, end_date))
                st.success("Period has been added.")
            else:
                st.warning("Please fill in the date fields.")

        # Display existing Periods
        st.write("### Existing Periods")
        rows = run_query("SELECT PeriodID, PlanID, PeriodSequence, StartDate, EndDate FROM Period;")
        df_period = pd.DataFrame(rows, columns=["PeriodID", "PlanID", "Sequence", "StartDate", "EndDate"])
        st.dataframe(df_period)

        # Update a Period
        st.write("### Update a Period")
        if not df_period.empty:
            period_ids = df_period["PeriodID"].tolist()
            selected_period_id = st.selectbox("Select Period ID to Update", period_ids)
            if selected_period_id:
                pdata = run_query(
                    "SELECT PlanID, PeriodSequence, StartDate, EndDate FROM Period WHERE PeriodID=?",
                    (selected_period_id,)
                )
                if pdata:
                    p_planid, p_seq, p_sdate, p_edate = pdata[0]
                    new_seq = st.number_input("New Period Sequence", min_value=1, value=p_seq)
                    new_start = st.text_input("New Start Date", value=p_sdate)
                    new_end = st.text_input("New End Date", value=p_edate)

                    if st.button("Update Period"):
                        upd_query = """
                        UPDATE Period
                        SET PeriodSequence=?, StartDate=?, EndDate=?
                        WHERE PeriodID=?
                        """
                        run_query(upd_query, (new_seq, new_start, new_end, selected_period_id))
                        st.success("Period updated successfully.")
                        st.experimental_rerun()

    # -------------------------------------------------------------------
    # PRODUCT MANAGEMENT
    # -------------------------------------------------------------------
    elif choice == "Product Management":
        st.subheader("Product Management")

        # Add a new product
        with st.form("product_form"):
            st.write("### Add a New Product")
            product_name = st.text_input("Product Name")
            product_type = st.text_input("Product Type", value="FinishedGood")
            lead_time = st.number_input("Lead Time", min_value=0, value=0)
            lot_size = st.number_input("Lot Size", min_value=1, value=1)
            on_hand = st.number_input("On-Hand Inventory", min_value=0, value=0)
            submitted = st.form_submit_button("Add Product")

        if submitted:
            if product_name and product_type:
                insert_q = """
                INSERT INTO Product (ProductName, ProductType, LeadTime, LotSize, OnHandInventory)
                VALUES (?, ?, ?, ?, ?)
                """
                run_query(insert_q, (product_name, product_type, lead_time, lot_size, on_hand))
                st.success(f"Product '{product_name}' has been added.")
            else:
                st.warning("Please fill in all fields.")

        # NOTE: The sections for displaying existing products or updating products
        # have been REMOVED to avoid any SELECT query that might cause the error.

    # -------------------------------------------------------------------
    # BOM MANAGEMENT
    # -------------------------------------------------------------------
    elif choice == "BOM Management":
        st.subheader("BOM (Bill of Materials) Management")

        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        prod_dict = {f"{r[1]} (ID: {r[0]})": r[0] for r in product_rows}

        with st.form("bom_form"):
            st.write("### Add a New BOM Entry")
            parent_sel = st.selectbox("Parent Product", list(prod_dict.keys()))
            child_sel = st.selectbox("Child Product", list(prod_dict.keys()))
            quantity = st.number_input("Quantity", min_value=0.1, value=1.0)
            level = st.number_input("Level", min_value=0, value=1)
            bom_submitted = st.form_submit_button("Add BOM Entry")

        if bom_submitted:
            parent_id = prod_dict[parent_sel]
            child_id = prod_dict[child_sel]
            if parent_id == child_id:
                st.error("Parent and Child cannot be the same product.")
            else:
                ins_bom = """
                INSERT INTO BOM (ParentProductID, ChildProductID, Quantity, Level)
                VALUES (?, ?, ?, ?)
                """
                run_query(ins_bom, (parent_id, child_id, quantity, level))
                st.success("BOM entry has been added.")

        # We still keep a BOM display if you want, or remove it similarly:
        st.write("### Existing BOM Entries")
        rows = run_query("""
            SELECT b.BomID, p1.ProductName AS Parent, p2.ProductName AS Child, 
                   b.Quantity, b.Level
            FROM BOM b
            JOIN Product p1 ON b.ParentProductID = p1.ProductID
            JOIN Product p2 ON b.ChildProductID = p2.ProductID
        """)
        df_bom = pd.DataFrame(rows, columns=["BomID", "Parent", "Child", "Quantity", "Level"])
        st.dataframe(df_bom)

    # -------------------------------------------------------------------
    # DEMAND / INVENTORY
    # -------------------------------------------------------------------
    elif choice == "Demand/Inventory":
        st.subheader("Demand / Inventory Management")

        plan_rows = run_query("SELECT PlanID, PlanName FROM Plan;")
        plan_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in plan_rows}

        period_rows = run_query("SELECT PeriodID, StartDate, EndDate FROM Period;")
        period_dict = {f"Period {r[0]} ({r[1]} - {r[2]})": r[0] for r in period_rows}

        product_rows = run_query("SELECT ProductID, ProductName FROM Product;")
        product_dict = {f"{r[1]} (ID: {r[0]})": r[0] for r in product_rows}

        with st.form("demand_form"):
            st.write("### Add Demand/Inventory Record")
            sel_plan = st.selectbox("Select Plan", list(plan_dict.keys()))
            sel_period = st.selectbox("Select Period", list(period_dict.keys()))
            sel_product = st.selectbox("Select Product", list(product_dict.keys()))
            gross_req = st.number_input("Gross Requirements", min_value=0.0, value=0.0)
            sched_receipts = st.number_input("Scheduled Receipts", min_value=0.0, value=0.0)
            proj_inv = st.number_input("Projected Inventory", min_value=0.0, value=0.0)
            net_req = st.number_input("Net Requirement", min_value=0.0, value=0.0)
            planned_order = st.number_input("Planned Order Releases", min_value=0.0, value=0.0)
            demand_submitted = st.form_submit_button("Add Record")

        if demand_submitted:
            plan_id = plan_dict[sel_plan]
            period_id = period_dict[sel_period]
            product_id = product_dict[sel_product]

            ins_demand = """
            INSERT INTO DemandInventory 
            (PlanID, PeriodID, ProductID, 
             GrossRequirements, ScheduledReceipts, 
             ProjectedInventory, NetRequirement, PlannedOrderReleases)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            run_query(ins_demand, (plan_id, period_id, product_id,
                                   gross_req, sched_receipts,
                                   proj_inv, net_req, planned_order))
            st.success("Demand/Inventory record has been added.")

        # Display existing Demand/Inventory
        st.write("### Existing DemandInventory Records")
        rows = run_query("""
            SELECT RecordID, PlanID, PeriodID, ProductID,
                   GrossRequirements, ScheduledReceipts,
                   ProjectedInventory, NetRequirement, PlannedOrderReleases
            FROM DemandInventory
        """)
        df_di = pd.DataFrame(rows, columns=[
            "RecordID","PlanID","PeriodID","ProductID",
            "GrossReq","ScheduledReceipts","ProjInventory","NetReq","PlannedOrder"
        ])
        st.dataframe(df_di)

    # -------------------------------------------------------------------
    # MRP CALCULATION
    # -------------------------------------------------------------------
    elif choice == "MRP Calculation":
        st.subheader("MRP Calculation")

        st.markdown("""
        Here we perform a simple MRP logic:
        - **NetRequirement** = max(0, GrossRequirements - (ProjectedInventory + ScheduledReceipts))
        - **PlannedOrderReleases** = NetRequirement (assuming lot-for-lot)
        """)

        if st.button("Run MRP Calculation"):
            # Update NetRequirement
            net_req_query = """
            UPDATE DemandInventory
            SET NetRequirement = CASE
                WHEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts)) > 0
                THEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts))
                ELSE 0
            END
            """
            run_query(net_req_query)

            # Update PlannedOrderReleases = NetRequirement
            plan_release_query = """
            UPDATE DemandInventory
            SET PlannedOrderReleases = NetRequirement
            """
            run_query(plan_release_query)

            st.success("MRP calculation completed.")

        # Display results
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

    # -------------------------------------------------------------------
    # ABOUT
    # -------------------------------------------------------------------
    else:
        st.subheader("About")
        st.markdown("""
        **This project** is a simple MRP (Material Requirements Planning) system 
        created for illustrative or educational purposes.  
        
        - **Database**: SQLite  
        - **Interface**: Streamlit  
        - **Features**: Manage Plans, Periods, BOM, Demand/Inventory, 
                       and run basic MRP calculations (lot-for-lot).
        """)

if __name__ == "__main__":
    main()
