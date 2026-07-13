-- =====================================================
-- E-Commerce Order Analytics System
-- Window Functions
-- =====================================================

---------------------------------------------------------
-- 1. Customer Revenue Ranking
---------------------------------------------------------

SELECT

    customer_id,

    customer_name,

    total_revenue,

    RANK() OVER(
        ORDER BY total_revenue DESC
    ) AS revenue_rank

FROM (

    SELECT

        c.customer_id,

        c.customer_name,

        ROUND(

            SUM(
                oi.quantity *
                oi.unit_price *
                (1 - oi.discount_percent/100.0)
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

);

---------------------------------------------------------
-- 2. Dense Rank Products
---------------------------------------------------------

SELECT

    product_id,

    product_name,

    revenue,

    DENSE_RANK() OVER(

        ORDER BY revenue DESC

    ) AS product_rank

FROM (

    SELECT

        p.product_id,

        p.product_name,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS revenue

    FROM products p

    JOIN order_items oi

    ON p.product_id=oi.product_id

    GROUP BY

        p.product_id,

        p.product_name

);

---------------------------------------------------------
-- 3. Running Revenue
---------------------------------------------------------

WITH monthly_sales AS (

SELECT

strftime('%Y-%m',o.order_date) AS sales_month,

ROUND(

SUM(

oi.quantity*
oi.unit_price*
(1-oi.discount_percent/100.0)

),

2

) AS revenue

FROM orders o

JOIN order_items oi

ON o.order_id=oi.order_id

GROUP BY sales_month

)

SELECT

sales_month,

revenue,

SUM(revenue) OVER(

ORDER BY sales_month

) AS running_revenue

FROM monthly_sales;

---------------------------------------------------------
-- 4. Moving Average Revenue (3 Months)
---------------------------------------------------------

WITH monthly_sales AS (

    SELECT

        strftime('%Y-%m', o.order_date) AS sales_month,

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

    GROUP BY sales_month

)

SELECT

    sales_month,

    revenue,

    ROUND(

        AVG(revenue) OVER (

            ORDER BY sales_month

            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW

        ),

        2

    ) AS moving_average

FROM monthly_sales;

---------------------------------------------------------
-- 5. Previous Order Date (LAG)
---------------------------------------------------------

SELECT

    customer_id,

    order_id,

    order_date,

    LAG(order_date) OVER (

        PARTITION BY customer_id

        ORDER BY order_date

    ) AS previous_order

FROM orders;

---------------------------------------------------------
-- 6. Next Order Date (LEAD)
---------------------------------------------------------

SELECT

    customer_id,

    order_id,

    order_date,

    LEAD(order_date) OVER (

        PARTITION BY customer_id

        ORDER BY order_date

    ) AS next_order

FROM orders;

---------------------------------------------------------
-- 7. Row Number by Customer
---------------------------------------------------------

SELECT

    customer_id,

    order_id,

    order_date,

    ROW_NUMBER() OVER (

        PARTITION BY customer_id

        ORDER BY order_date

    ) AS order_sequence

FROM orders;

---------------------------------------------------------
-- 8. Customer Quartiles (NTILE)
---------------------------------------------------------

WITH customer_revenue AS (

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

SELECT

    customer_id,

    customer_name,

    revenue,

    NTILE(4) OVER (

        ORDER BY revenue DESC

    ) AS revenue_quartile

FROM customer_revenue;

---------------------------------------------------------
-- 9. Top 3 Products in Each Category
---------------------------------------------------------

WITH product_sales AS (

    SELECT

        p.category,

        p.product_id,

        p.product_name,

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

        p.category,

        p.product_id,

        p.product_name

)

SELECT *

FROM (

    SELECT

        *,

        ROW_NUMBER() OVER (

            PARTITION BY category

            ORDER BY revenue DESC

        ) AS rank_in_category

    FROM product_sales

)

WHERE rank_in_category <= 3

ORDER BY category, rank_in_category;