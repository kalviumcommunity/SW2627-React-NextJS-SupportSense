-- Purpose: Consolidate customer profile with their high-level transaction history.
-- Business metric: total_orders and lifetime_value per customer.
-- Source tables: customers, orders
-- Important columns: customer_id, customer_name, customer_type, total_orders, lifetime_value
-- Intended consumers: Dashboard User Profile page, REST API user lookup.

CREATE VIEW IF NOT EXISTS vw_customer_order_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_type,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COALESCE(SUM(o.order_amount), 0) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, 
    c.customer_name, 
    c.customer_type;
