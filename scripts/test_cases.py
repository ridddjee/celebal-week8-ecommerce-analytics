"""
=========================================================
Project : E-Commerce Order Analytics System
File    : test_cases.py

Description:
Basic automated validation for the project.
=========================================================
"""

import sqlite3
from pathlib import Path
import pandas as pd

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "ecommerce.db"

CLEAN_DIR = BASE_DIR / "data" / "cleaned"


# =====================================================
# Test Functions
# =====================================================

def test_database_exists():

    assert DATABASE_PATH.exists(), \
        "Database file not found."

    print("✓ Database Exists")


def test_customer_count():

    df = pd.read_csv(
        CLEAN_DIR / "customers.csv"
    )

    assert len(df) > 0

    print("✓ Customers Loaded")


def test_product_count():

    df = pd.read_csv(
        CLEAN_DIR / "products.csv"
    )

    assert len(df) > 0

    print("✓ Products Loaded")


def test_orders_count():

    df = pd.read_csv(
        CLEAN_DIR / "orders.csv"
    )

    assert len(df) > 0

    print("✓ Orders Loaded")


def test_order_items_count():

    df = pd.read_csv(
        CLEAN_DIR / "order_items.csv"
    )

    assert len(df) > 0

    print("✓ Order Items Loaded")


def test_duplicate_primary_keys():

    customers = pd.read_csv(
        CLEAN_DIR / "customers.csv"
    )

    products = pd.read_csv(
        CLEAN_DIR / "products.csv"
    )

    orders = pd.read_csv(
        CLEAN_DIR / "orders.csv"
    )

    items = pd.read_csv(
        CLEAN_DIR / "order_items.csv"
    )

    assert customers["customer_id"].duplicated().sum() == 0
    assert products["product_id"].duplicated().sum() == 0
    assert orders["order_id"].duplicated().sum() == 0
    assert items["item_id"].duplicated().sum() == 0

    print("✓ Primary Keys Unique")


def test_foreign_keys():

    conn = sqlite3.connect(DATABASE_PATH)

    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_key_check")

    result = cursor.fetchall()

    conn.close()

    assert len(result) == 0

    print("✓ Foreign Keys Valid")


def test_negative_prices():

    df = pd.read_csv(
        CLEAN_DIR / "order_items.csv"
    )

    assert (df["unit_price"] >= 0).all()

    print("✓ Prices Valid")


def test_discount_range():

    df = pd.read_csv(
        CLEAN_DIR / "order_items.csv"
    )

    assert (
        (df["discount_percent"] >= 0)
        &
        (df["discount_percent"] <= 100)
    ).all()

    print("✓ Discount Range Valid")


# =====================================================
# Main
# =====================================================

def main():

    print("=" * 60)
    print("RUNNING PROJECT TESTS")
    print("=" * 60)

    test_database_exists()
    test_customer_count()
    test_product_count()
    test_orders_count()
    test_order_items_count()
    test_duplicate_primary_keys()
    test_foreign_keys()
    test_negative_prices()
    test_discount_range()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()