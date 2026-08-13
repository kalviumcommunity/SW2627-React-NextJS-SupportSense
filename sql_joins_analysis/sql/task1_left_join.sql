-- Task 1: LEFT JOIN with Aggregation
-- Purpose: Combine customers with their orders, keeping all customers even if they have no orders.
-- This uses a LEFT JOIN to ensure C05 (Eve), who has no orders, is still included in the result.
-- Because customer C01 has multiple orders (O101, O102), joining the tables multiplies the customer row.
-- We then GROUP BY the customer to aggregate the metrics.

SELECT 
    c.customer_id, 
    c.customer_type,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.order_amount) AS total_spent
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY 
    c.customer_id, 
    c.customer_type;
