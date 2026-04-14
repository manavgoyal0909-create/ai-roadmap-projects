import sqlite3
import pandas as pd

# ── 1. CREATE DATABASE ────────────────────────────────────────
# This creates a local database file called shop.db
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

print("=" * 50)
print("Creating tables...")
print("=" * 50)


# ── 2. CREATE 3 TABLES ───────────────────────────────────────

# Table 1: Customers
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    city          TEXT,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Table 2: Products
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id    INTEGER PRIMARY KEY,
    product_name  TEXT NOT NULL,
    category      TEXT,
    price         REAL NOT NULL,
    stock         INTEGER DEFAULT 0
)
""")

# Table 3: Orders (links customers + products)
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL,
    order_date    TEXT DEFAULT CURRENT_TIMESTAMP,
    status        TEXT DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
)
""")

print("3 tables created successfully!")


# ── 3. INSERT SAMPLE DATA ────────────────────────────────────

# Add customers
cursor.executemany("""
INSERT OR IGNORE INTO customers (customer_id, name, email, city)
VALUES (?, ?, ?, ?)
""", [
    (1, "Ravi Sharma",   "ravi@email.com",   "Jaipur"),
    (2, "Priya Singh",   "priya@email.com",  "Delhi"),
    (3, "Amit Verma",    "amit@email.com",   "Mumbai"),
    (4, "Sunita Mehta",  "sunita@email.com", "Jaipur"),
    (5, "Deepak Kumar",  "deepak@email.com", "Pune"),
])

# Add products
cursor.executemany("""
INSERT OR IGNORE INTO products (product_id, product_name, category, price, stock)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, "Laptop",      "Electronics", 55000, 10),
    (2, "Mobile",      "Electronics", 15000, 25),
    (3, "Headphones",  "Electronics",  2500, 50),
    (4, "Desk Chair",  "Furniture",    8000, 15),
    (5, "Notebook",    "Stationery",    150, 200),
])

# Add orders
cursor.executemany("""
INSERT OR IGNORE INTO orders (order_id, customer_id, product_id, quantity, status)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, 1, 2, 1, "delivered"),
    (2, 2, 1, 1, "delivered"),
    (3, 3, 3, 2, "pending"),
    (4, 1, 5, 5, "delivered"),
    (5, 4, 4, 1, "shipped"),
    (6, 5, 2, 2, "pending"),
    (7, 2, 3, 1, "delivered"),
])

conn.commit()
print("Sample data inserted!")


# ── 4. QUERY THE DATA ────────────────────────────────────────

print()
print("=" * 50)
print("ALL CUSTOMERS")
print("=" * 50)
df_customers = pd.read_sql("SELECT * FROM customers", conn)
print(df_customers)

print()
print("=" * 50)
print("ALL PRODUCTS")
print("=" * 50)
df_products = pd.read_sql("SELECT * FROM products", conn)
print(df_products)

print()
print("=" * 50)
print("ALL ORDERS WITH CUSTOMER + PRODUCT NAMES")
print("=" * 50)
query = """
SELECT 
    o.order_id,
    c.name        AS customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    (o.quantity * p.price) AS total_amount,
    o.status
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
"""
df_orders = pd.read_sql(query, conn)
print(df_orders)


# ── 5. BUSINESS INSIGHTS ─────────────────────────────────────

print()
print("=" * 50)
print("BUSINESS INSIGHTS")
print("=" * 50)

# Total revenue per customer
print("\nTotal spent per customer:")
revenue_query = """
SELECT 
    c.name,
    COUNT(o.order_id)            AS total_orders,
    SUM(o.quantity * p.price)    AS total_spent
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products  p ON o.product_id  = p.product_id
GROUP BY c.name
ORDER BY total_spent DESC
"""
df_revenue = pd.read_sql(revenue_query, conn)
print(df_revenue)

# Most popular product
print("\nMost ordered products:")
popular_query = """
SELECT 
    p.product_name,
    SUM(o.quantity) AS total_sold
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sold DESC
"""
df_popular = pd.read_sql(popular_query, conn)
print(df_popular)

# Orders by city
print("\nOrders by city:")
city_query = """
SELECT 
    c.city,
    COUNT(o.order_id) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY total_orders DESC
"""
df_city = pd.read_sql(city_query, conn)
print(df_city)


# ── 6. CLOSE CONNECTION ──────────────────────────────────────
conn.close()
print()
print("Database saved as shop.db ✅")