-- Task 4: Multi-Table JOIN
-- Purpose: Join customers, orders, order_items, and products to calculate line totals.
-- Filtered only for 'Enterprise' customers.

SELECT 
    c.customer_id, 
    c.customer_type, 
    o.order_id, 
    o.order_date, 
    p.product_id, 
    p.product_name, 
    i.quantity, 
    i.unit_price, 
    (i.quantity * i.unit_price) AS line_total
FROM customers c
INNER JOIN orders o 
    ON c.customer_id = o.customer_id
INNER JOIN order_items i 
    ON o.order_id = i.order_id
INNER JOIN products p 
    ON i.product_id = p.product_id
WHERE c.customer_type = 'Enterprise';
