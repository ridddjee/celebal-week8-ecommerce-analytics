"""
=========================================================
Project : E-Commerce Order Analytics System
File    : load_database.py
Author  : Ridam Agrawal

Description:
Creates SQLite database and loads cleaned CSV files.
=========================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd
import logging
import traceback

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "ecommerce.db"

SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"

CLEAN_DIR = BASE_DIR / "data" / "cleaned"

# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# Database Connection
# =====================================================

def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


# =====================================================
# Create Schema
# =====================================================

def create_schema(conn):

    logger.info("Creating schema...")

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        conn.executescript(f.read())

    conn.commit()

    logger.info("Schema created successfully.")


# =====================================================
# Load One Table
# =====================================================

def load_table(
    conn,
    csv_file,
    table_name
):

    print("\n" + "=" * 60)
    print(f"Loading {table_name}")
    print("=" * 60)

    df = pd.read_csv(csv_file)

    print(f"Rows Found : {len(df)}")

    cursor = conn.cursor()

    columns = list(df.columns)

    placeholders = ",".join(
        ["?"] * len(columns)
    )

    sql = f"""
    INSERT INTO {table_name}
    ({",".join(columns)})
    VALUES ({placeholders})
    """

    inserted = 0

    for index, row in df.iterrows():

        try:

            cursor.execute(
                sql,
                tuple(row)
            )

            inserted += 1

        except Exception as e:

            print("\nFAILED RECORD")
            print("-" * 40)

            print(f"Table : {table_name}")

            print(f"CSV Row : {index+2}")

            print(row.to_dict())

            print("\nSQLite Error")

            print(e)

            raise

    conn.commit()

    print(f"Inserted : {inserted}")

    return inserted


# =====================================================
# Validate Table
# =====================================================

def validate_table(
    conn,
    table_name
):

    cursor = conn.cursor()

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    return cursor.fetchone()[0]


# =====================================================
# Database Summary
# =====================================================

def database_summary(conn):

    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)

    tables = [
        "customers",
        "products",
        "orders",
        "order_items"
    ]

    for table in tables:

        rows = validate_table(
            conn,
            table
        )

        print(f"{table:<15}: {rows}")


# =====================================================
# Load Database
# =====================================================

def load_database():

    conn = get_connection()

    try:

        create_schema(conn)

        print("\nStarting Database Loading...\n")

        load_table(
            conn,
            CLEAN_DIR / "customers.csv",
            "customers"
        )

        print("✓ customers loaded")

        load_table(
            conn,
            CLEAN_DIR / "products.csv",
            "products"
        )

        print("✓ products loaded")

        load_table(
            conn,
            CLEAN_DIR / "orders.csv",
            "orders"
        )

        print("✓ orders loaded")

        load_table(
            conn,
            CLEAN_DIR / "order_items.csv",
            "order_items"
        )

        print("✓ order_items loaded")

        database_summary(conn)

        print("\n" + "=" * 60)
        print("DATABASE CREATED SUCCESSFULLY")
        print("=" * 60)

        print(f"\nSQLite File : {DATABASE_PATH}")

        conn.close()

    except Exception:

        print("\n" + "=" * 60)
        print("DATABASE LOADING FAILED")
        print("=" * 60)

        traceback.print_exc()

        conn.rollback()

        conn.close()

        raise


# =====================================================
# Main
# =====================================================

def main():

    try:

        load_database()

    except Exception as e:

        logger.exception(e)

        print("\nProgram Stopped.")


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()