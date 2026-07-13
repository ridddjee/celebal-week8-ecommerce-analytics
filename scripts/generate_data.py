"""
=========================================================
Project : E-Commerce Order Analytics System
File    : generate_data.py
Author  : Ridam Agrawal

Description:
Generate realistic e-commerce datasets with intentional
data quality issues for ETL processing.
=========================================================
"""

from pathlib import Path
from faker import Faker
import pandas as pd
import random
import logging
from datetime import datetime, timedelta

# =====================================================
# Configuration
# =====================================================

fake = Faker("en_IN")

random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# Dataset Sizes
# =====================================================

TOTAL_CUSTOMERS = 1000
TOTAL_PRODUCTS = 500
TOTAL_ORDERS = 5000

MIN_ITEMS = 1
MAX_ITEMS = 5

# =====================================================
# Static Data
# =====================================================

CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

REGIONS = [
    "NORTH",
    "SOUTH",
    "EAST",
    "WEST"
]

PRODUCT_CATALOG = {
    "Electronics": {
        "subcategory": [
            "Mobile",
            "Laptop",
            "Accessories",
            "Tablet"
        ],
        "products": [
            "iPhone 15",
            "Samsung Galaxy S24",
            "MacBook Air M3",
            "Dell Inspiron",
            "Sony Headphones",
            "Logitech Mouse",
            "Apple Watch",
            "HP Pavilion",
            "Lenovo ThinkPad",
            "Boat Earbuds"
        ],
        "price": (15000, 120000)
    },

    "Clothing": {
        "subcategory": [
            "Men",
            "Women",
            "Kids"
        ],
        "products": [
            "Cotton T-Shirt",
            "Hoodie",
            "Blue Jeans",
            "Jacket",
            "Sneakers",
            "Sports Shoes",
            "Casual Shirt",
            "Formal Shirt",
            "Track Pant",
            "Kurta"
        ],
        "price": (500, 8000)
    },

    "Home": {
        "subcategory": [
            "Kitchen",
            "Furniture",
            "Decor"
        ],
        "products": [
            "Dining Table",
            "Office Chair",
            "Microwave",
            "Mixer Grinder",
            "Sofa",
            "Curtains",
            "LED Lamp",
            "Wall Clock",
            "Pressure Cooker",
            "Water Bottle"
        ],
        "price": (500, 25000)
    },

    "Books": {
        "subcategory": [
            "Education",
            "Biography",
            "Fiction"
        ],
        "products": [
            "Python Programming",
            "SQL Mastery",
            "Data Engineering",
            "Machine Learning",
            "Deep Learning",
            "Atomic Habits",
            "Rich Dad Poor Dad",
            "Think and Grow Rich",
            "Harry Potter",
            "The Alchemist"
        ],
        "price": (250, 2500)
    }
}

# =====================================================
# Helper Functions
# =====================================================

def random_registration_date():
    """Generate registration date."""

    return fake.date_between(
        start_date="-3y",
        end_date="-30d"
    )


def random_order_date():
    """Generate realistic order datetime."""

    start = datetime.now() - timedelta(days=730)

    random_days = random.randint(0, 730)

    dt = start + timedelta(
        days=random_days,
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

    return dt


def generate_customer_id(index):
    return f"C{index:05}"


def generate_product_id(index):
    return f"P{index:04}"


def generate_order_id(index):
    return f"O{index:06}"


def generate_item_id(index):
    return f"I{index:07}"


def make_invalid_email(email):
    """Create invalid email."""

    if random.random() < 0.5:
        return email.replace("@", "")

    return email.split("@")[0] + "@"

# =====================================================
# Customer Generation
# =====================================================

def generate_customers():
    """
    Generate customer master data.
    """

    logger.info("Generating customers...")

    customers = []

    for i in range(1, TOTAL_CUSTOMERS + 1):

        customer_id = generate_customer_id(i)

        customer_name = fake.name()

        email = fake.email()

        # 2% Invalid Emails
        if random.random() < 0.02:
            email = make_invalid_email(email)

        customer_type = random.choices(
            CUSTOMER_TYPES,
            weights=[70, 20, 10],
            k=1
        )[0]

        customers.append({

            "customer_id": customer_id,

            "customer_name": customer_name,

            "email": email,

            "registration_date": random_registration_date(),

            "customer_type": customer_type

        })

    logger.info("Customers Generated : %s", len(customers))

    return pd.DataFrame(customers)


# =====================================================
# Product Helpers
# =====================================================

def random_product_name(name):
    """
    Introduce mixed casing and spaces.
    """

    r = random.random()

    if r < 0.25:
        return name.upper()

    elif r < 0.50:
        return name.lower()

    elif r < 0.75:
        return "  " + name + "  "

    return name


def generate_cost_price(category):

    low, high = PRODUCT_CATALOG[category]["price"]

    return round(random.uniform(low, high), 2)


# =====================================================
# Product Generation
# =====================================================

def generate_products():

    logger.info("Generating products...")

    products = []

    product_counter = 1

    for category, details in PRODUCT_CATALOG.items():

        base_products = details["products"]

        subcategories = details["subcategory"]

        while len(
            [p for p in products if p["category"] == category]
        ) < 125:

            product_name = random.choice(base_products)

            product_name = random_product_name(product_name)

            products.append({

                "product_id": generate_product_id(product_counter),

                "product_name": product_name,

                "category": category,

                "subcategory": random.choice(subcategories),

                "cost_price": generate_cost_price(category)

            })

            product_counter += 1

    logger.info("Products Generated : %s", len(products))

    return pd.DataFrame(products)


# =====================================================
# Customer Lookup Helper
# =====================================================

def customer_pool(customers_df):

    return customers_df["customer_id"].tolist()


# =====================================================
# Product Lookup Helper
# =====================================================

def random_product(products_df):

    row = products_df.sample(1).iloc[0]

    return {

        "product_id": row["product_id"],

        "cost_price": row["cost_price"],

        "category": row["category"]

    }


# =====================================================
# Price Calculation
# =====================================================

def selling_price(cost):

    markup = random.uniform(1.20, 1.80)

    return round(cost * markup, 2)


# =====================================================
# Discount
# =====================================================

def random_discount():

    return round(random.uniform(0, 50), 2)


# =====================================================
# Quantity
# =====================================================

def random_quantity():

    qty = random.randint(1, 5)

    # 3% Negative Quantity (Returns)

    if random.random() < 0.03:

        qty *= -1

    return qty

# =====================================================
# Order Generation
# =====================================================

def generate_orders(customers_df, products_df):

    logger.info("Generating orders...")

    customer_ids = customer_pool(customers_df)

    orders = []
    order_items = []

    item_counter = 1

    for order_no in range(1, TOTAL_ORDERS + 1):

        order_id = generate_order_id(order_no)

        customer_id = random.choice(customer_ids)

        # -------------------------------------------------
        # 5% Missing Customer IDs
        # -------------------------------------------------

        if random.random() < 0.05:
            customer_id = ""

        # -------------------------------------------------
        # Order Date
        # -------------------------------------------------

        order_datetime = random_order_date()

        # 2% Wrong Date Format
        if random.random() < 0.02:

            order_date = order_datetime.strftime(
                "%d-%m-%Y %H:%M:%S"
            )

        else:

            order_date = order_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        # -------------------------------------------------
        # Order Status
        # -------------------------------------------------

        status = random.choices(

            ORDER_STATUS,

            weights=[
                12,
                20,
                55,
                8,
                5
            ],

            k=1

        )[0]

        # -------------------------------------------------
        # Region
        # -------------------------------------------------

        region = random.choice(REGIONS)

        # -------------------------------------------------
        # Save Order
        # -------------------------------------------------

        orders.append({

            "order_id": order_id,

            "customer_id": customer_id,

            "order_date": order_date,

            "status": status,

            "region_code": region

        })

        # =================================================
        # Order Items
        # =================================================

        number_of_items = random.randint(
            MIN_ITEMS,
            MAX_ITEMS
        )

        for _ in range(number_of_items):

            product = random_product(products_df)

            quantity = random_quantity()

            unit_price = selling_price(
                product["cost_price"]
            )

            discount = random_discount()

            order_items.append({

                "item_id":
                    generate_item_id(item_counter),

                "order_id":
                    order_id,

                "product_id":
                    product["product_id"],

                "quantity":
                    quantity,

                "unit_price":
                    unit_price,

                "discount_percent":
                    discount

            })

            item_counter += 1

    logger.info(
        "Orders Generated : %s",
        len(orders)
    )

    logger.info(
        "Order Items Generated : %s",
        len(order_items)
    )

    orders_df = pd.DataFrame(orders)

    order_items_df = pd.DataFrame(order_items)

    return orders_df, order_items_df


# =====================================================
# Save CSV
# =====================================================

def save_dataframe(df, filename):

    path = RAW_DIR / filename

    df.to_csv(
        path,
        index=False
    )

    logger.info(
        "%s saved successfully.",
        filename
    )
    # =====================================================
# Main
# =====================================================

def main():

    logger.info("=" * 60)
    logger.info("Starting Data Generation")
    logger.info("=" * 60)

    try:

        # -----------------------------------------------
        # Generate Customers
        # -----------------------------------------------

        customers_df = generate_customers()

        # -----------------------------------------------
        # Generate Products
        # -----------------------------------------------

        products_df = generate_products()

        # -----------------------------------------------
        # Generate Orders & Order Items
        # -----------------------------------------------

        orders_df, order_items_df = generate_orders(
            customers_df,
            products_df
        )

        # -----------------------------------------------
        # Export CSV Files
        # -----------------------------------------------

        save_dataframe(
            customers_df,
            "customers.csv"
        )

        save_dataframe(
            products_df,
            "products.csv"
        )

        save_dataframe(
            orders_df,
            "orders.csv"
        )

        save_dataframe(
            order_items_df,
            "order_items.csv"
        )

        # -----------------------------------------------
        # Summary
        # -----------------------------------------------

        print("\n" + "=" * 60)
        print("DATA GENERATION COMPLETED")
        print("=" * 60)

        print(f"Customers     : {len(customers_df)}")
        print(f"Products      : {len(products_df)}")
        print(f"Orders        : {len(orders_df)}")
        print(f"Order Items   : {len(order_items_df)}")

        print("\nCSV Files Saved To:")

        print(RAW_DIR)

        print("\nGenerated Files")

        print("✔ customers.csv")
        print("✔ products.csv")
        print("✔ orders.csv")
        print("✔ order_items.csv")

        print("\nIntentional Data Quality Issues Added")

        print("✔ 5% Missing Customer IDs")
        print("✔ 3% Negative Quantities")
        print("✔ 2% Invalid Emails")
        print("✔ Mixed Product Names")
        print("✔ Wrong Date Formats")

        logger.info("Data Generation Completed Successfully.")

    except Exception as e:

        logger.exception("Generation Failed")

        print("\nERROR")

        print(str(e))


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    main()