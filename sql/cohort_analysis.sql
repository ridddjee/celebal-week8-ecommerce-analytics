-- =====================================================
-- E-Commerce Order Analytics System
-- Cohort Analysis + CTE + RFM Segmentation
-- =====================================================

---------------------------------------------------------
-- 1. Customer First Purchase (CTE)
---------------------------------------------------------

WITH first_purchase AS (

    SELECT

        customer_id,

        MIN(order_date) AS first_order_date

    FROM orders

    WHERE customer_id IS NOT NULL

    GROUP BY customer_id

)

SELECT *

FROM first_purchase

ORDER BY first_order_date;

---------------------------------------------------------
-- 2. Monthly Cohort
---------------------------------------------------------

WITH first_purchase AS (

    SELECT

        customer_id,

        MIN(order_date) AS first_order_date

    FROM orders

    WHERE customer_id IS NOT NULL

    GROUP BY customer_id

)

SELECT

    strftime('%Y-%m', first_order_date) AS cohort_month,

    COUNT(*) AS total_customers

FROM first_purchase

GROUP BY cohort_month

ORDER BY cohort_month;

---------------------------------------------------------
-- 3. Customer Retention Matrix
---------------------------------------------------------

WITH first_purchase AS (

    SELECT

        customer_id,

        MIN(order_date) AS first_order_date

    FROM orders

    WHERE customer_id IS NOT NULL

    GROUP BY customer_id

),

customer_orders AS (

    SELECT

        o.customer_id,

        strftime('%Y-%m', fp.first_order_date) AS cohort,

        strftime('%Y-%m', o.order_date) AS order_month

    FROM orders o

    JOIN first_purchase fp

    ON o.customer_id = fp.customer_id

)

SELECT

    cohort,

    order_month,

    COUNT(DISTINCT customer_id) AS retained_customers

FROM customer_orders

GROUP BY

    cohort,

    order_month

ORDER BY

    cohort,

    order_month;

---------------------------------------------------------
-- 4. Customer Lifetime Value
---------------------------------------------------------

WITH customer_sales AS (

SELECT

c.customer_id,

c.customer_name,

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

) AS lifetime_value

FROM customers c

JOIN orders o

ON c.customer_id=o.customer_id

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY

c.customer_id,

c.customer_name

)

SELECT

customer_id,

customer_name,

ROUND(lifetime_value,2) AS lifetime_value

FROM customer_sales

ORDER BY lifetime_value DESC;


---------------------------------------------------------
-- 5. RFM Analysis
---------------------------------------------------------

WITH customer_metrics AS (

    SELECT

        c.customer_id,

        c.customer_name,

        MAX(o.order_date) AS last_order,

        COUNT(DISTINCT o.order_id) AS frequency,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)

            ),

            2

        ) AS monetary

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY

        c.customer_id,

        c.customer_name

)

SELECT

    customer_id,

    customer_name,

    CAST(
        julianday('now') - julianday(last_order)
        AS INTEGER
    ) AS recency,

    frequency,

    monetary

FROM customer_metrics

ORDER BY monetary DESC;

---------------------------------------------------------
-- 6. Customer Segmentation
---------------------------------------------------------

WITH customer_metrics AS (

    SELECT

        c.customer_id,

        c.customer_name,

        MAX(o.order_date) AS last_order,

        COUNT(DISTINCT o.order_id) AS frequency,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent / 100.0)

            ),

            2

        ) AS monetary

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY

        c.customer_id,

        c.customer_name

)

SELECT

    customer_id,

    customer_name,

    frequency,

    monetary,

    CASE

        WHEN monetary >= 100000
             AND frequency >= 10
        THEN 'VIP'

        WHEN monetary >= 50000
        THEN 'LOYAL'

        WHEN frequency >= 5
        THEN 'REGULAR'

        ELSE 'NEW'

    END AS customer_segment

FROM customer_metrics

ORDER BY monetary DESC;

---------------------------------------------------------
-- 7. Top 20 High Value Customers
---------------------------------------------------------

WITH customer_sales AS (

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

        ) AS revenue

    FROM customers c

    JOIN orders o
        ON c.customer_id = o.customer_id

    JOIN order_items oi
        ON o.order_id = oi.order_id

    GROUP BY

        c.customer_id,

        c.customer_name

)

SELECT *

FROM customer_sales

ORDER BY revenue DESC

LIMIT 20;

---------------------------------------------------------
-- 8. Dormant Customers
---------------------------------------------------------

SELECT

    customer_id,

    customer_name,

    registration_date

FROM customers

WHERE customer_id NOT IN (

    SELECT DISTINCT customer_id

    FROM orders

    WHERE customer_id IS NOT NULL

);

---------------------------------------------------------
-- 9. Repeat Customers
---------------------------------------------------------

SELECT

    customer_id,

    COUNT(order_id) AS total_orders

FROM orders

WHERE customer_id IS NOT NULL

GROUP BY customer_id

HAVING COUNT(order_id) > 1

ORDER BY total_orders DESC;