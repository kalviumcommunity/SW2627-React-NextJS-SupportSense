-- Query 1: INNER JOIN
-- Purpose: Returns only the intersection. Excludes customers without orders and orphaned orders.
SELECT 
    c.customer_id, 
    c.customer_name, 
    o.order_id, 
    o.order_amount
FROM customers c
INNER JOIN orders o 
    ON c.customer_id = o.customer_id;

-- Query 2: LEFT JOIN
-- Purpose: Returns all customers, including those without orders. Orphaned orders are excluded.
SELECT 
    c.customer_id, 
    c.customer_name, 
    o.order_id, 
    o.order_amount
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id;

-- Query 3: FULL OUTER JOIN Equivalent (UNION Approach)
-- Purpose: Returns all customers and all orders.
-- This uses a UNION ALL of a LEFT JOIN and a RIGHT-equivalent JOIN to ensure compatibility 
-- with databases like older SQLite that do not natively support FULL OUTER JOIN.
SELECT 
    c.customer_id, 
    c.customer_name, 
    o.order_id, 
    o.order_amount
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
UNION ALL
SELECT 
    NULL AS customer_id, 
    NULL AS customer_name, 
    o.order_id, 
    o.order_amount
FROM orders o
LEFT JOIN customers c 
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
