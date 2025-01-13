-- create_tables.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ProductPeriod;
DROP TABLE IF EXISTS BOM;
DROP TABLE IF EXISTS PlanPeriod;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Period;
DROP TABLE IF EXISTS Plan;

CREATE TABLE Plan (
    PlanID           INTEGER PRIMARY KEY, 
    PlanName         TEXT    NOT NULL,
    PlanStartDate    TEXT    NOT NULL,
    PlanEndDate      TEXT    NOT NULL,
    PlanningHorizon  INTEGER NOT NULL,
    PlanStatus       TEXT
);

CREATE TABLE Period (
    PeriodID         INTEGER PRIMARY KEY,
    PeriodSequence   INTEGER NOT NULL,
    PeriodStartDate  TEXT    NOT NULL,
    PeriodEndDate    TEXT    NOT NULL
);

CREATE TABLE PlanPeriod (
    PlanID   INTEGER NOT NULL,
    PeriodID INTEGER NOT NULL,
    CapacityConstraint REAL,
    Notes    TEXT,
    PRIMARY KEY (PlanID, PeriodID),
    FOREIGN KEY (PlanID)   REFERENCES Plan(PlanID),
    FOREIGN KEY (PeriodID) REFERENCES Period(PeriodID)
);

CREATE TABLE Product (
    ProductID        INTEGER PRIMARY KEY,
    ProductName      TEXT    NOT NULL,
    ProductType      TEXT,
    LeadTime         INTEGER NOT NULL,
    LotSize          INTEGER NOT NULL,
    OnHandInventory  INTEGER NOT NULL
);

CREATE TABLE BOM (
    ParentProductID  INTEGER NOT NULL,
    ChildProductID   INTEGER NOT NULL,
    Quantity         REAL    NOT NULL,
    Level            INTEGER NOT NULL,
    PRIMARY KEY (ParentProductID, ChildProductID),
    FOREIGN KEY (ParentProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (ChildProductID)  REFERENCES Product(ProductID)
);

CREATE TABLE ProductPeriod (
    ProductID         INTEGER NOT NULL,
    PeriodID          INTEGER NOT NULL,
    PlanID            INTEGER NOT NULL,
    GrossRequirements    REAL NOT NULL DEFAULT 0,
    ScheduledReceipts    REAL NOT NULL DEFAULT 0,
    ProjectedInventory   REAL NOT NULL DEFAULT 0,
    NetRequirement       REAL NOT NULL DEFAULT 0,
    PlannedOrderReleases REAL NOT NULL DEFAULT 0,
    PRIMARY KEY (ProductID, PeriodID, PlanID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
    FOREIGN KEY (PeriodID) REFERENCES Period(PeriodID),
    FOREIGN KEY (PlanID)   REFERENCES Plan(PlanID)
);
