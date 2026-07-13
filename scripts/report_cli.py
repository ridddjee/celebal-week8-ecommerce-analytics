"""
=========================================================
Project : E-Commerce Order Analytics System
File    : report_cli.py
Author  : Ridam Agrawal

Description:
Interactive CLI Reporting Tool
=========================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd
from tabulate import tabulate

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

OUTPUT_DIR = BASE_DIR / "output" / "sample_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Database Connection
# =====================================================

def get_connection():

    return sqlite3.connect(DATABASE_PATH)


# =====================================================
# Execute SQL
# =====================================================

def run_query(query):

    conn = get_connection()

    df = pd.read_sql_query(

        query,

        conn

    )

    conn.close()

    return df


# =====================================================
# Pretty Print
# =====================================================

def show(df):

    if df.empty:

        print("\nNo Data Found.\n")

        return

    print()

    print(

        tabulate(

            df,

            headers="keys",

            tablefmt="grid",

            showindex=False

        )

    )

    print()


# =====================================================
# Export CSV
# =====================================================

def export(df, filename):

    path = OUTPUT_DIR / filename

    df.to_csv(

        path,

        index=False

    )

    print(f"\nReport Exported -> {path}\n")

    # =====================================================
# Dashboard Summary
# =====================================================

def dashboard_summary():

    query = """
    SELECT

        (SELECT COUNT(*) FROM customers) AS total_customers,

        (SELECT COUNT(*) FROM products) AS total_products,

        (SELECT COUNT(*) FROM orders) AS total_orders,

        ROUND(
            (
                SELECT SUM(
                    quantity *
                    unit_price *
                    (1-discount_percent/100.0)
                )
                FROM order_items
            ),
            2
        ) AS total_revenue;
    """

    df = run_query(query)

    print("\n" + "=" * 60)
    print("E-COMMERCE DASHBOARD")
    print("=" * 60)

    show(df)


# =====================================================
# Monthly Revenue
# =====================================================

def monthly_revenue():

    query = """
    SELECT

        strftime('%Y-%m',o.order_date) AS Month,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS Revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id=oi.order_id

    GROUP BY Month

    ORDER BY Month;
    """

    df = run_query(query)

    print("\nMONTHLY REVENUE\n")

    show(df)

    export(

        df,

        "monthly_revenue.csv"

    )


# =====================================================
# Revenue by Category
# =====================================================

def revenue_by_category():

    query = """
    SELECT

        p.category,

        ROUND(

            SUM(

                oi.quantity*
                oi.unit_price*
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS Revenue

    FROM products p

    JOIN order_items oi

    ON p.product_id=oi.product_id

    GROUP BY p.category

    ORDER BY Revenue DESC;
    """

    df = run_query(query)

    print("\nCATEGORY REVENUE\n")

    show(df)

    export(

        df,

        "category_revenue.csv"

    )


# =====================================================
# Revenue by Region
# =====================================================

def revenue_by_region():

    query = """
    SELECT

        o.region_code,

        ROUND(

            SUM(

                oi.quantity*
                oi.unit_price*
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS Revenue

    FROM orders o

    JOIN order_items oi

    ON o.order_id=oi.order_id

    GROUP BY o.region_code

    ORDER BY Revenue DESC;
    """

    df = run_query(query)

    print("\nREGION REVENUE\n")

    show(df)

    export(

        df,

        "region_revenue.csv"

    )

    # =====================================================
# Top 10 Customers
# =====================================================

def top_customers():

    query = """
    SELECT

        c.customer_id,

        c.customer_name,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS Revenue

    FROM customers c

    JOIN orders o

        ON c.customer_id=o.customer_id

    JOIN order_items oi

        ON o.order_id=oi.order_id

    GROUP BY

        c.customer_id,

        c.customer_name

    ORDER BY Revenue DESC

    LIMIT 10;
    """

    df = run_query(query)

    print("\nTOP 10 CUSTOMERS\n")

    show(df)

    export(
        df,
        "top_customers.csv"
    )


# =====================================================
# Top 10 Products
# =====================================================

def top_products():

    query = """
    SELECT

        p.product_id,

        p.product_name,

        p.category,

        ROUND(

            SUM(

                oi.quantity *
                oi.unit_price *
                (1-oi.discount_percent/100.0)

            ),

            2

        ) AS Revenue

    FROM products p

    JOIN order_items oi

        ON p.product_id=oi.product_id

    GROUP BY

        p.product_id,

        p.product_name,

        p.category

    ORDER BY Revenue DESC

    LIMIT 10;
    """

    df = run_query(query)

    print("\nTOP 10 PRODUCTS\n")

    show(df)

    export(
        df,
        "top_products.csv"
    )


# =====================================================
# Customer Segmentation
# =====================================================

def customer_segments():

    query = """
    WITH customer_sales AS (

        SELECT

            c.customer_id,

            c.customer_name,

            COUNT(DISTINCT o.order_id) AS Orders,

            ROUND(

                SUM(

                    oi.quantity *
                    oi.unit_price *
                    (1-oi.discount_percent/100.0)

                ),

                2

            ) AS Revenue

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

        Orders,

        Revenue,

        CASE

            WHEN Revenue >= 100000
                 AND Orders >= 10
            THEN 'VIP'

            WHEN Revenue >= 50000
            THEN 'LOYAL'

            WHEN Orders >= 5
            THEN 'REGULAR'

            ELSE 'NEW'

        END AS Segment

    FROM customer_sales

    ORDER BY Revenue DESC;
    """

    df = run_query(query)

    print("\nCUSTOMER SEGMENTS\n")

    show(df)

    export(
        df,
        "customer_segments.csv"
    )


# =====================================================
# Orders by Status
# =====================================================

def order_status_report():

    query = """
    SELECT

        status,

        COUNT(*) AS Total_Orders

    FROM orders

    GROUP BY status

    ORDER BY Total_Orders DESC;
    """

    df = run_query(query)

    print("\nORDER STATUS REPORT\n")

    show(df)

    export(
        df,
        "order_status.csv"
    )

    # =====================================================
# CLI Menu
# =====================================================

def print_menu():

    print("\n" + "=" * 60)
    print("E-COMMERCE ORDER ANALYTICS SYSTEM")
    print("=" * 60)

    print("1. Dashboard Summary")
    print("2. Monthly Revenue")
    print("3. Revenue by Category")
    print("4. Revenue by Region")
    print("5. Top 10 Customers")
    print("6. Top 10 Products")
    print("7. Customer Segmentation")
    print("8. Order Status Report")
    print("9. Run All Reports")
    print("0. Exit")

    print("=" * 60)


# =====================================================
# Execute Menu Option
# =====================================================

def execute_choice(choice):

    if choice == "1":

        dashboard_summary()

    elif choice == "2":

        monthly_revenue()

    elif choice == "3":

        revenue_by_category()

    elif choice == "4":

        revenue_by_region()

    elif choice == "5":

        top_customers()

    elif choice == "6":

        top_products()

    elif choice == "7":

        customer_segments()

    elif choice == "8":

        order_status_report()

    elif choice == "9":

        print("\nGenerating All Reports...\n")

        dashboard_summary()

        monthly_revenue()

        revenue_by_category()

        revenue_by_region()

        top_customers()

        top_products()

        customer_segments()

        order_status_report()

        print("\nAll reports generated successfully.\n")

    elif choice == "0":

        print("\nThank you for using the E-Commerce Analytics System.")

        return False

    else:

        print("\nInvalid choice. Please enter a number between 0 and 9.")

    return True


# =====================================================
# CLI Loop
# =====================================================

def start_cli():

    running = True

    while running:

        print_menu()

        choice = input("\nEnter your choice: ").strip()

        running = execute_choice(choice)

        # =====================================================
# Main
# =====================================================

def main():

    print("\n" + "=" * 60)
    print("E-COMMERCE ORDER ANALYTICS SYSTEM")
    print("Celebal Technologies - Week 8 Final Project")
    print("=" * 60)

    # ---------------------------------------------
    # Check Database
    # ---------------------------------------------

    if not DATABASE_PATH.exists():

        print("\nERROR")
        print("-" * 40)
        print("Database not found.")
        print("Run the following scripts first:")
        print("\n1. python scripts/generate_data.py")
        print("2. python scripts/clean_data.py")
        print("3. python scripts/load_database.py\n")
        return

    try:

        start_cli()

    except KeyboardInterrupt:

        print("\n\nProgram terminated by user.")

    except Exception as error:

        print("\nUnexpected Error")
        print("-" * 40)

        print(type(error).__name__)

        print(error)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":

    main()