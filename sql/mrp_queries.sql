-- mrp_queries.sql

-- Net Requirement = max(0, GrossRequirements - (ProjectedInventory + ScheduledReceipts))
UPDATE ProductPeriod
SET NetRequirement = CASE
    WHEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts)) > 0
    THEN (GrossRequirements - (ProjectedInventory + ScheduledReceipts))
    ELSE 0
END;

-- Planned Order Releases = Net Requirement (lot-for-lot)
UPDATE ProductPeriod
SET PlannedOrderReleases = NetRequirement;
