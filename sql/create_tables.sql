-- create_tables.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS DemandInventory;
DROP TABLE IF EXISTS BOM;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Period;
DROP TABLE IF EXISTS Plan;

/* ----------------------
   1) Plan Tablosu
----------------------- */
CREATE TABLE IF NOT EXISTS Plan (
    PlanID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanName TEXT NOT NULL,
    StartDate TEXT NOT NULL,
    PeriodType TEXT NOT NULL,
    PlanningHorizon INTEGER NOT NULL
);

/* ----------------------
   2) Period Tablosu
----------------------- */
CREATE TABLE IF NOT EXISTS Period (
    PeriodID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanID INTEGER,
    PeriodSequence INTEGER NOT NULL,
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID)
);

/* ----------------------
   3) Product Tablosu
----------------------- */
CREATE TABLE IF NOT EXISTS Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    ProductType TEXT NOT NULL,          -- 'FinishedGood', 'RawMaterial', vs.
    LeadTime INTEGER NOT NULL DEFAULT 0,
    LotSize INTEGER NOT NULL DEFAULT 1,
    OnHandInventory INTEGER NOT NULL DEFAULT 0
);

/* ----------------------
   4) BOM (Bill of Materials) Tablosu
----------------------- */
CREATE TABLE IF NOT EXISTS BOM (
    BomID INTEGER PRIMARY KEY AUTOINCREMENT,
    ParentProductID INTEGER NOT NULL,
    ChildProductID INTEGER NOT NULL,
    Quantity REAL NOT NULL,
    Level INTEGER NOT NULL,
    FOREIGN KEY (ParentProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (ChildProductID) REFERENCES Product(ProductID)
);

/* ----------------------
   5) DemandInventory Tablosu
----------------------- */
CREATE TABLE IF NOT EXISTS DemandInventory (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanID INTEGER NOT NULL,
    PeriodID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    GrossRequirements REAL NOT NULL DEFAULT 0,
    ScheduledReceipts REAL NOT NULL DEFAULT 0,
    ProjectedInventory REAL NOT NULL DEFAULT 0,
    NetRequirement REAL NOT NULL DEFAULT 0,
    PlannedOrderReleases REAL NOT NULL DEFAULT 0,
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID),
    FOREIGN KEY (PeriodID) REFERENCES Period(PeriodID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
