-- insert_sample_data.sql

INSERT INTO Plan (PlanID, PlanName, PlanStartDate, PlanEndDate, PlanningHorizon, PlanStatus)
VALUES 
(1, '2025_MainPlan', '2025-01-01', '2025-12-31', 12, 'Draft');

INSERT INTO Period (PeriodID, PeriodSequence, PeriodStartDate, PeriodEndDate)
VALUES
(1, 1, '2025-01-01', '2025-01-07'),
(2, 2, '2025-01-08', '2025-01-14'),
(3, 3, '2025-01-15', '2025-01-21');

INSERT INTO PlanPeriod (PlanID, PeriodID, CapacityConstraint, Notes)
VALUES
(1, 1, 1000.0, 'Week1 capacity'),
(1, 2, 1200.0, 'Week2 capacity'),
(1, 3, 900.0,  'Week3 capacity');

INSERT INTO Product (ProductID, ProductName, ProductType, LeadTime, LotSize, OnHandInventory)
VALUES
(100, 'Widget A', 'FinishedGood', 2, 50, 20),
(200, 'Widget B', 'FinishedGood', 2, 50, 15),
(300, 'Material X', 'RawMaterial', 1, 100, 100);

INSERT INTO BOM (ParentProductID, ChildProductID, Quantity, Level)
VALUES
(100, 300, 2.0, 1), -- A needs 2 X
(200, 300, 3.0, 1); -- B needs 3 X

INSERT INTO ProductPeriod (ProductID, PeriodID, PlanID, GrossRequirements, ScheduledReceipts)
VALUES
(100, 1, 1, 10, 0),
(100, 2, 1, 15, 0),
(200, 1, 1, 5, 5),
(300, 1, 1, 0, 20);  -- raw material with scheduled receipt

