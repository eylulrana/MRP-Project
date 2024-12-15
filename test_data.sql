

INSERT INTO Plan (PlanName, StartDate, PeriodType, PlanningHorizon) VALUES 
('September Plan', '2023-09-01', 'Monthly', 12);

INSERT INTO Period (PlanID, PeriodSequence, StartDate, EndDate) VALUES
(1, 1, '2023-09-01', '2023-09-30'),
(1, 2, '2023-10-01', '2023-10-31');

INSERT INTO Product (ProductName, ProductType) VALUES
('Car', 'Finished Product'),
('Wheel', 'Component');

INSERT INTO BOM (ParentProductID, ChildProductID, Quantity, Level) VALUES
(1, 2, 4, 1);

INSERT INTO DemandInventory (PlanID, PeriodID, ProductID, GrossRequirements, ScheduledReceipts, ProjectedInventory) VALUES
(1, 1, 1, 500, 200, 100);
