-- Purpose: Monitor product sales performance.
-- Business metric: total_quantity_sold and total_product_revenue per product.
-- Source tables: products, order_items
-- Important columns: product_id, product_name, category, total_quantity_sold, total_product_revenue
-- Intended consumers: Dashboard Inventory page, REST API product metrics.

CREATE VIEW IF NOT EXISTS vw_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COALESCE(SUM(i.quantity), 0) AS total_quantity_sold,
    COALESCE(SUM(i.quantity * i.unit_price), 0) AS total_product_revenue
FROM products p
LEFT JOIN order_items i ON p.product_id = i.product_id
GROUP BY 
    p.product_id, 
    p.product_name, 
    p.category;
