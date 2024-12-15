

CREATE TABLE IF NOT EXISTS Plan (
    PlanID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanName TEXT NOT NULL,
    StartDate TEXT NOT NULL,
    PeriodType TEXT NOT NULL,
    PlanningHorizon INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Period (
    PeriodID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanID INTEGER,
    PeriodSequence INTEGER NOT NULL,
    StartDate TEXT NOT NULL,
    EndDate TEXT NOT NULL,
    FOREIGN KEY (PlanID) REFERENCES Plan (PlanID)
);

CREATE TABLE IF NOT EXISTS Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    ProductType TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS BOM (
    BomID INTEGER PRIMARY KEY AUTOINCREMENT,
    ParentProductID INTEGER,
    ChildProductID INTEGER,
    Quantity INTEGER NOT NULL,
    Level INTEGER,
    FOREIGN KEY (ParentProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (ChildProductID) REFERENCES Product(ProductID)
);

CREATE TABLE IF NOT EXISTS DemandInventory (
    RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
    PlanID INTEGER,
    PeriodID INTEGER,
    ProductID INTEGER,
    GrossRequirements INTEGER,
    ScheduledReceipts INTEGER,
    ProjectedInventory INTEGER,
    NetRequirement INTEGER,
    PlannedOrderReleases INTEGER,
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID),
    FOREIGN KEY (PeriodID) REFERENCES Period(PeriodID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
