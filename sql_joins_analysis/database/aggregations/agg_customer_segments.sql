-- Purpose: Pre-aggregate segment performance metrics.
-- Business metric: customer_count, total_segment_revenue per customer segment.
-- Source tables: vw_customer_order_summary
-- Important columns: customer_type, customer_count, total_segment_revenue, updated_at
-- Intended consumers: Dashboard Segments Chart, REST API segments metrics.

CREATE TABLE IF NOT EXISTS agg_customer_segments (
    customer_type VARCHAR(50) PRIMARY KEY,
    customer_count INTEGER,
    total_segment_revenue NUMERIC(12,2),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full refresh logic
DELETE FROM agg_customer_segments;

INSERT INTO agg_customer_segments (customer_type, customer_count, total_segment_revenue, updated_at)
SELECT 
    customer_type,
    COUNT(customer_id) AS customer_count,
    SUM(lifetime_value) AS total_segment_revenue,
    CURRENT_TIMESTAMP
FROM vw_customer_order_summary
GROUP BY customer_type;
