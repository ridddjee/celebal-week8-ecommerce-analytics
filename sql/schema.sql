-- =====================================================
-- E-Commerce Order Analytics System
-- SQLite Database Schema
-- Celebal Technologies Week-8 Final Project
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- Customers
-- =====================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    registration_date DATE NOT NULL,
    customer_type TEXT NOT NULL
        CHECK(customer_type IN ('REGULAR','PREMIUM','VIP'))
);

-- =====================================================
-- Products
-- =====================================================

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    cost_price REAL NOT NULL
        CHECK(cost_price >= 0)
);

-- =====================================================
-- Orders
-- =====================================================

CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,

    customer_id TEXT,

    order_date DATETIME NOT NULL,

    status TEXT NOT NULL
        CHECK(status IN
        (
            'PLACED',
            'SHIPPED',
            'DELIVERED',
            'CANCELLED',
            'RETURNED'
        )),

    region_code TEXT NOT NULL,

    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

-- =====================================================
-- Order Items
-- =====================================================

CREATE TABLE order_items (

    item_id TEXT PRIMARY KEY,

    order_id TEXT NOT NULL,

    product_id TEXT NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price REAL NOT NULL
        CHECK(unit_price >= 0),

    discount_percent REAL NOT NULL
        CHECK(discount_percent BETWEEN 0 AND 100),

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =====================================================
-- Helpful Indexes
-- =====================================================

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_orders_status
ON orders(status);

CREATE INDEX idx_products_category
ON products(category);

CREATE INDEX idx_items_order
ON order_items(order_id);

CREATE INDEX idx_items_product
ON order_items(product_id);