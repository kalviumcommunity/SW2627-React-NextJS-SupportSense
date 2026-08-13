-- Query 1: Customers without orders
-- Purpose: Find customers who exist in the customers table but have no matching records in orders.
SELECT 
    c.customer_id, 
    c.customer_name, 
    c.customer_type
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- Query 2: Orphaned orders
-- Purpose: Find orders where the customer_id does not exist in the customers table.
SELECT 
    o.order_id, 
    o.customer_id, 
    o.order_date, 
    o.order_amount
FROM orders o
LEFT JOIN customers c 
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
