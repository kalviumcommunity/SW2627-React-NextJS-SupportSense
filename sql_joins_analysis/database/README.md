# SQL Data Layer

This directory serves as the centralized, single source of truth for business metrics, built to prevent metric drift across dashboards, backend APIs, and notebooks.

## Why SQL Views?
SQL Views (`vw_`) encapsulate complex JOIN logic and business rules into a single virtual table. This ensures that a dashboard and a backend service querying "Active Customers" will always get exactly the same results, without developers needing to re-write complex JOINs.

## Why Aggregation Tables?
Aggregation tables (`agg_`) pre-calculate expensive computations (e.g., daily revenue sums). Instead of the dashboard summing millions of raw rows on every page load, it simply selects the pre-computed day from the `agg_daily_revenue` table.

## Naming Conventions
- `vw_`: SQL Views (Virtual tables, evaluated at query time)
- `agg_`: Pre-Aggregated tables (Physical tables, requires refresh)

## Existing Views
- **`vw_customer_order_summary`**: Customer profile + lifetime value and order counts.
- **`vw_product_performance`**: Product inventory details + total quantities sold and revenue.

## Existing Aggregations
- **`agg_daily_revenue`**: Time-series grain of daily financial performance.
- **`agg_customer_segments`**: Categorical grain of revenue by customer type (Enterprise, SMB, Startup).

## Refresh Strategy
Currently, all `agg_` tables use a **Full Refresh** strategy (`DELETE` followed by `INSERT`).
- **Why**: The dataset is small enough that a full table scan and rewrite is near-instantaneous. It avoids complex merge logic or duplicate prevention mechanisms.
- **When**: This should be triggered by the Backend (e.g., Node.js cron job) nightly or immediately after the raw data ingestion pipeline completes.

## Future Consumption
When the Express backend and React dashboard are built:
1. React Dashboard will request `/api/metrics/daily-revenue`
2. Express will query `SELECT * FROM agg_daily_revenue ORDER BY aggregation_date DESC`
3. The data is already perfectly formatted for JSON serialization and Chart.js plotting. No calculation is performed in Node.js.
