"""
=========================================================
Project : E-Commerce Order Analytics System
File    : clean_data.py
Author  : Ridam Agrawal

Description:
Clean raw datasets, validate data quality,
maintain referential integrity,
and export cleaned CSV files.
=========================================================
"""

from pathlib import Path
import pandas as pd
import logging
import re

# =====================================================
# Project Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CLEAN_DIR = BASE_DIR / "data" / "cleaned"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Logging
# =====================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger(__name__)

# =====================================================
# Issue Tracker
# =====================================================

issues = []


def log_issue(issue_type, record_id, details):

    issues.append({

        "issue_type": issue_type,

        "record_id": record_id,

        "details": details

    })


# =====================================================
# Email Validation
# =====================================================

EMAIL_PATTERN = re.compile(

    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

)


# =====================================================
# Date Parsing
# =====================================================

def parse_date(value):

    if pd.isna(value):

        return pd.NaT

    formats = [

        "%Y-%m-%d %H:%M:%S",

        "%d-%m-%Y %H:%M:%S"

    ]

    for fmt in formats:

        try:

            return pd.to_datetime(

                value,

                format=fmt

            )

        except Exception:

            pass

    return pd.NaT


# =====================================================
# Load Raw Files
# =====================================================

def load_raw_files():

    logger.info("Loading Raw CSV Files")

    customers = pd.read_csv(

        RAW_DIR / "customers.csv"

    )

    products = pd.read_csv(

        RAW_DIR / "products.csv"

    )

    orders = pd.read_csv(

        RAW_DIR / "orders.csv"

    )

    order_items = pd.read_csv(

        RAW_DIR / "order_items.csv"

    )

    return (

        customers,

        products,

        orders,

        order_items

    )


# =====================================================
# Customer Cleaning
# =====================================================

def clean_customers(df):

    logger.info("Cleaning Customers")

    df["customer_name"] = (

        df["customer_name"]

        .astype(str)

        .str.strip()

        .str.title()

    )

    df["email"] = (

        df["email"]

        .astype(str)

        .str.strip()

        .str.lower()

    )

    invalid = []

    for _, row in df.iterrows():

        if not EMAIL_PATTERN.match(row["email"]):

            invalid.append(row["customer_id"])

            log_issue(

                "INVALID_EMAIL",

                row["customer_id"],

                row["email"]

            )

    logger.info(

        "Invalid Emails : %s",

        len(invalid)

    )

    return df

# =====================================================
# Product Cleaning
# =====================================================

def clean_products(df):

    logger.info("Cleaning Products")

    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    df["category"] = (
        df["category"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["subcategory"] = (
        df["subcategory"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    )

    invalid_price = df["cost_price"].isna()

    for _, row in df.loc[invalid_price].iterrows():

        log_issue(
            "INVALID_PRICE",
            row["product_id"],
            "Invalid cost price"
        )

    df = df.dropna(subset=["cost_price"])

    df = df[df["cost_price"] >= 0]

    return df


# =====================================================
# Orders Cleaning
# =====================================================

def clean_orders(df, customers_df):

    logger.info("Cleaning Orders")

    original_dates = df["order_date"].copy()

    df["order_date"] = df["order_date"].apply(
        parse_date
    )

    invalid_dates = df["order_date"].isna()

    for order_id, old_date in zip(
        df.loc[invalid_dates, "order_id"],
        original_dates.loc[invalid_dates]
    ):

        log_issue(
            "INVALID_DATE",
            order_id,
            f"Invalid date: {old_date}"
        )

    # Remove rows with invalid dates
    df = df.dropna(subset=["order_date"])

    # Convert blank customer IDs to NULL
    df["customer_id"] = (
        df["customer_id"]
        .replace("", pd.NA)
    )

    # Existing customer IDs
    valid_customers = set(
        customers_df["customer_id"]
    )

    # Invalid foreign keys
    invalid_customer_rows = df[
        df["customer_id"].notna() &
        ~df["customer_id"].isin(valid_customers)
    ]

    for _, row in invalid_customer_rows.iterrows():

        log_issue(
            "INVALID_CUSTOMER",
            row["order_id"],
            f"Customer ID {row['customer_id']} not found"
        )

    # Keep NULL customer_id OR valid customer_id
    df = df[
        df["customer_id"].isna() |
        df["customer_id"].isin(valid_customers)
    ]

    return df.reset_index(drop=True)


# =====================================================
# Order Items Cleaning
# =====================================================

def clean_order_items(order_items_df, orders_df, products_df):

    logger.info("Cleaning Order Items")

    # Numeric conversions
    order_items_df["quantity"] = pd.to_numeric(
        order_items_df["quantity"],
        errors="coerce"
    )

    order_items_df["unit_price"] = pd.to_numeric(
        order_items_df["unit_price"],
        errors="coerce"
    )

    order_items_df["discount_percent"] = pd.to_numeric(
        order_items_df["discount_percent"],
        errors="coerce"
    )

    # Remove invalid numeric rows
    order_items_df = order_items_df.dropna(
        subset=[
            "quantity",
            "unit_price",
            "discount_percent"
        ]
    )

    # Quantity cannot be zero
    invalid_qty = order_items_df["quantity"] == 0

    for _, row in order_items_df.loc[invalid_qty].iterrows():

        log_issue(
            "INVALID_QUANTITY",
            row["item_id"],
            "Quantity cannot be zero"
        )

    order_items_df = order_items_df[
        order_items_df["quantity"] != 0
    ]

    # Price validation
    order_items_df = order_items_df[
        order_items_df["unit_price"] >= 0
    ]

    # Discount validation
    order_items_df = order_items_df[
        (order_items_df["discount_percent"] >= 0) &
        (order_items_df["discount_percent"] <= 100)
    ]

    # ---------------------------------------------
    # Foreign Key Validation
    # ---------------------------------------------

    valid_orders = set(
        orders_df["order_id"]
    )

    valid_products = set(
        products_df["product_id"]
    )

    invalid_order_rows = order_items_df[
        ~order_items_df["order_id"].isin(valid_orders)
    ]

    for _, row in invalid_order_rows.iterrows():

        log_issue(
            "INVALID_ORDER_REFERENCE",
            row["item_id"],
            row["order_id"]
        )

    invalid_product_rows = order_items_df[
        ~order_items_df["product_id"].isin(valid_products)
    ]

    for _, row in invalid_product_rows.iterrows():

        log_issue(
            "INVALID_PRODUCT_REFERENCE",
            row["item_id"],
            row["product_id"]
        )

    # Keep only valid rows
    order_items_df = order_items_df[

        order_items_df["order_id"].isin(valid_orders)

    ]

    order_items_df = order_items_df[

        order_items_df["product_id"].isin(valid_products)

    ]

    return order_items_df.reset_index(drop=True)


# =====================================================
# Save Clean Files
# =====================================================

def save_clean_file(df, filename):

    output_path = CLEAN_DIR / filename

    df.to_csv(

        output_path,

        index=False

    )

    logger.info(

        "%s saved successfully.",

        filename

    )


# =====================================================
# Save Issues Report
# =====================================================

def save_issues():

    issues_df = pd.DataFrame(issues)

    issues_df.to_csv(

        CLEAN_DIR / "issues_report.csv",

        index=False

    )

    logger.info(

        "issues_report.csv saved."

    )
    # =====================================================
# Main Cleaning Pipeline
# =====================================================

def clean_data():

    logger.info("=" * 60)
    logger.info("Starting Data Cleaning")
    logger.info("=" * 60)

    (
        customers_df,
        products_df,
        orders_df,
        order_items_df
    ) = load_raw_files()

    # -------------------------------------------------
    # Customers
    # -------------------------------------------------

    customers_df = clean_customers(
        customers_df
    )

    # -------------------------------------------------
    # Products
    # -------------------------------------------------

    products_df = clean_products(
        products_df
    )

    # -------------------------------------------------
    # Orders
    # -------------------------------------------------

    orders_df = clean_orders(
        orders_df,
        customers_df
    )

    # -------------------------------------------------
    # Order Items
    # -------------------------------------------------

    order_items_df = clean_order_items(
        order_items_df,
        orders_df,
        products_df
    )

    # -------------------------------------------------
    # Convert Date Format
    # -------------------------------------------------

    orders_df["order_date"] = (
        pd.to_datetime(
            orders_df["order_date"]
        )
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    # -------------------------------------------------
    # Remove Duplicate Primary Keys
    # -------------------------------------------------

    customers_df = customers_df.drop_duplicates(
        subset=["customer_id"]
    )

    products_df = products_df.drop_duplicates(
        subset=["product_id"]
    )

    orders_df = orders_df.drop_duplicates(
        subset=["order_id"]
    )

    order_items_df = order_items_df.drop_duplicates(
        subset=["item_id"]
    )

    # -------------------------------------------------
    # Export Clean Files
    # -------------------------------------------------

    save_clean_file(
        customers_df,
        "customers.csv"
    )

    save_clean_file(
        products_df,
        "products.csv"
    )

    save_clean_file(
        orders_df,
        "orders.csv"
    )

    save_clean_file(
        order_items_df,
        "order_items.csv"
    )

    save_issues()

    logger.info("=" * 60)
    logger.info("Cleaning Finished")
    logger.info("=" * 60)

    return {

        "customers": len(customers_df),

        "products": len(products_df),

        "orders": len(orders_df),

        "order_items": len(order_items_df),

        "issues": len(issues)

    }
# =====================================================
# Main
# =====================================================

def main():

    try:

        summary = clean_data()

        print("\n" + "=" * 60)
        print("DATA CLEANING COMPLETED")
        print("=" * 60)

        print(f"Customers        : {summary['customers']}")
        print(f"Products         : {summary['products']}")
        print(f"Orders           : {summary['orders']}")
        print(f"Order Items      : {summary['order_items']}")
        print(f"Issues Logged    : {summary['issues']}")

        print("\nGenerated Files")
        print("----------------------------")
        print("✔ customers.csv")
        print("✔ products.csv")
        print("✔ orders.csv")
        print("✔ order_items.csv")
        print("✔ issues_report.csv")

        print("\nOutput Location")
        print("----------------------------")
        print(CLEAN_DIR)

        logger.info("=" * 60)
        logger.info("Cleaning Completed Successfully")
        logger.info("=" * 60)

    except Exception as e:

        logger.exception("Cleaning Failed")

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)
        print(type(e).__name__)
        print(e)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()