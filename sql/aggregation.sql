-- =====================================================
-- E-Commerce Order Analytics System
-- Aggregation Queries
-- =====================================================

---------------------------------------------------------
-- 1. Total Revenue
---------------------------------------------------------

SELECT
    ROUND(
        SUM(
            quantity *
            unit_price *
            (1 - discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items;

---------------------------------------------------------
-- 2. Total Orders
---------------------------------------------------------

SELECT
    COUNT(*) AS total_orders
FROM orders;

---------------------------------------------------------
-- 3. Total Customers
---------------------------------------------------------

SELECT
    COUNT(*) AS total_customers
FROM customers;

---------------------------------------------------------
-- 4. Total Products
---------------------------------------------------------

SELECT
    COUNT(*) AS total_products
FROM products;

---------------------------------------------------------
-- 5. Revenue by Category
---------------------------------------------------------

SELECT

    p.category,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS revenue

FROM order_items oi

JOIN products p

ON oi.product_id = p.product_id

GROUP BY p.category

ORDER BY revenue DESC;

---------------------------------------------------------
-- 6. Orders by Status
---------------------------------------------------------

SELECT

    status,

    COUNT(*) AS total_orders

FROM orders

GROUP BY status

ORDER BY total_orders DESC;


---------------------------------------------------------
-- 7. Top 10 Customers by Revenue
---------------------------------------------------------

SELECT

    c.customer_id,

    c.customer_name,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS total_revenue

FROM customers c

JOIN orders o

ON c.customer_id = o.customer_id

JOIN order_items oi

ON o.order_id = oi.order_id

GROUP BY

    c.customer_id,

    c.customer_name

ORDER BY total_revenue DESC

LIMIT 10;

---------------------------------------------------------
-- 8. Top 10 Products by Revenue
---------------------------------------------------------

SELECT

    p.product_id,

    p.product_name,

    p.category,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS revenue

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY

    p.product_id,

    p.product_name,

    p.category

ORDER BY revenue DESC

LIMIT 10;

---------------------------------------------------------
-- 9. Monthly Revenue
---------------------------------------------------------

SELECT

    strftime('%Y-%m', o.order_date) AS month,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id = oi.order_id

GROUP BY month

ORDER BY month;

---------------------------------------------------------
-- 10. Average Order Value
---------------------------------------------------------

WITH order_totals AS (

    SELECT

        o.order_id,

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ) AS order_value

    FROM orders o

    JOIN order_items oi

    ON o.order_id = oi.order_id

    GROUP BY o.order_id

)

SELECT

    ROUND(

        AVG(order_value),

        2

    ) AS average_order_value

FROM order_totals;

---------------------------------------------------------
-- 11. Region Wise Revenue
---------------------------------------------------------

SELECT

    o.region_code,

    ROUND(

        SUM(

            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)

        ),

        2

    ) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id = oi.order_id

GROUP BY o.region_code

ORDER BY revenue DESC;

---------------------------------------------------------
-- 12. Category Wise Quantity Sold
---------------------------------------------------------

SELECT

    p.category,

    SUM(oi.quantity) AS quantity_sold

FROM products p

JOIN order_items oi

ON p.product_id = oi.product_id

GROUP BY p.category

ORDER BY quantity_sold DESC;