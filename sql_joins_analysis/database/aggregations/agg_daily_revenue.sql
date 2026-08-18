-- Purpose: Pre-aggregate daily revenue metrics for fast dashboard rendering.
-- Business metric: total_revenue, order_count, avg_order_value per day.
-- Source tables: orders
-- Important columns: aggregation_date, total_revenue, order_count, avg_order_value, updated_at
-- Intended consumers: Dashboard Revenue Chart, REST API daily metrics.

CREATE TABLE IF NOT EXISTS agg_daily_revenue (
    aggregation_date DATE PRIMARY KEY,
    total_revenue NUMERIC(12,2),
    order_count INTEGER,
    avg_order_value NUMERIC(10,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full refresh logic
DELETE FROM agg_daily_revenue;

INSERT INTO agg_daily_revenue (aggregation_date, total_revenue, order_count, avg_order_value, updated_at)
SELECT 
    order_date AS aggregation_date,
    SUM(order_amount) AS total_revenue,
    COUNT(order_id) AS order_count,
    ROUND(SUM(order_amount) / COUNT(order_id), 2) AS avg_order_value,
    CURRENT_TIMESTAMP
FROM orders
GROUP BY order_date;
