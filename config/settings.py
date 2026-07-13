"""
=========================================================
Project : E-Commerce Order Analytics System
Author  : Ridam Agrawal
Company : Celebal Technologies
Purpose : Centralized project configuration
=========================================================
"""

from pathlib import Path
import logging

# =========================================================
# Project Root
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =========================================================
# Directories
# =========================================================

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

CLEAN_DATA_DIR = DATA_DIR / "cleaned"

DATABASE_DIR = PROJECT_ROOT / "database"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = OUTPUT_DIR / "sample_reports"

LOG_DIR = PROJECT_ROOT / "logs"

SQL_DIR = PROJECT_ROOT / "sql"

# =========================================================
# Database
# =========================================================

DATABASE_NAME = "ecommerce.db"

DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# =========================================================
# CSV Files
# =========================================================

CUSTOMERS_FILE = RAW_DATA_DIR / "customers.csv"

PRODUCTS_FILE = RAW_DATA_DIR / "products.csv"

ORDERS_FILE = RAW_DATA_DIR / "orders.csv"

ORDER_ITEMS_FILE = RAW_DATA_DIR / "order_items.csv"

# =========================================================
# Clean CSV Files
# =========================================================

CLEAN_CUSTOMERS_FILE = CLEAN_DATA_DIR / "customers.csv"

CLEAN_PRODUCTS_FILE = CLEAN_DATA_DIR / "products.csv"

CLEAN_ORDERS_FILE = CLEAN_DATA_DIR / "orders.csv"

CLEAN_ORDER_ITEMS_FILE = CLEAN_DATA_DIR / "order_items.csv"

ISSUES_REPORT_FILE = CLEAN_DATA_DIR / "issues_report.csv"

# =========================================================
# Dataset Size
# =========================================================

TOTAL_CUSTOMERS = 1000

TOTAL_PRODUCTS = 500

TOTAL_ORDERS = 5000

MIN_ITEMS_PER_ORDER = 1

MAX_ITEMS_PER_ORDER = 5

# =========================================================
# Data Quality Rules
# =========================================================

NULL_CUSTOMER_PERCENT = 5

NEGATIVE_QUANTITY_PERCENT = 3

INVALID_EMAIL_PERCENT = 2

INVALID_DATE_PERCENT = 2

# =========================================================
# Random Seed
# =========================================================

RANDOM_SEED = 42

# =========================================================
# Customer Types
# =========================================================

CUSTOMER_TYPES = [
    "REGULAR",
    "PREMIUM",
    "VIP"
]

# =========================================================
# Order Status
# =========================================================

ORDER_STATUS = [
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "RETURNED"
]

# =========================================================
# Categories
# =========================================================

PRODUCT_CATEGORIES = {

    "Electronics": [
        "Laptop",
        "Mobile",
        "Accessories",
        "Tablet"
    ],

    "Clothing": [
        "Men",
        "Women",
        "Kids"
    ],

    "Home": [
        "Kitchen",
        "Furniture",
        "Decor"
    ],

    "Books": [
        "Fiction",
        "Education",
        "Biography"
    ]
}

# =========================================================
# Regions
# =========================================================

REGIONS = [
    "North",
    "South",
    "East",
    "West"
]

# =========================================================
# Logging
# =========================================================

LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(

    filename=LOG_DIR / "project.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"
)

LOGGER = logging.getLogger("ECommerceAnalytics")

# =========================================================
# Create Required Directories
# =========================================================

for folder in [

    RAW_DATA_DIR,

    CLEAN_DATA_DIR,

    DATABASE_DIR,

    OUTPUT_DIR,

    REPORT_DIR,

    LOG_DIR

]:

    folder.mkdir(parents=True, exist_ok=True)