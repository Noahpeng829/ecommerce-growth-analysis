import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

# ==============================
# 1. fact_orders
# 1 row = 1 order
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE fact_orders AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    o.order_status,

    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_timestamp,
    CAST(o.order_approved_at AS TIMESTAMP) AS order_approved_at,
    CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS order_delivered_carrier_date,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS order_delivered_customer_date,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_date,

    DATE_DIFF(
        'day',
        CAST(o.order_purchase_timestamp AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) AS actual_delivery_days,

    DATE_DIFF(
        'day',
        CAST(o.order_estimated_delivery_date AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) AS delivery_delay_days,

    CASE
        WHEN o.order_delivered_customer_date IS NULL THEN NULL
        WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP)
             > CAST(o.order_estimated_delivery_date AS TIMESTAMP)
        THEN 1
        ELSE 0
    END AS is_delayed,

    r.review_score,

    EXTRACT(year FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_year,
    EXTRACT(month FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
    DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month_date

FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN order_reviews r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered';
""")

# ==============================
# 2. fact_order_items
# 1 row = 1 order item
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE fact_order_items AS
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    oi.shipping_limit_date
FROM order_items oi
INNER JOIN orders o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered';
""")

# ==============================
# 3. fact_payments
# 1 row = 1 payment record
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE fact_payments AS
SELECT
    pay.order_id,
    pay.payment_sequential,
    pay.payment_type,
    pay.payment_installments,
    pay.payment_value
FROM order_payments pay
INNER JOIN orders o
    ON pay.order_id = o.order_id
WHERE o.order_status = 'delivered';
""")

# ==============================
# 4. dim_customers
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE dim_customers AS
SELECT DISTINCT
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM customers;
""")

# ==============================
# 5. dim_products
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE dim_products AS
SELECT DISTINCT
    p.product_id,
    p.product_category_name,
    COALESCE(pct.product_category_name_english, 'Unknown') AS product_category_name_english,
    p.product_name_lenght,
    p.product_description_lenght,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM products p
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name;
""")

# ==============================
# 6. dim_sellers
# ==============================
conn.execute("""
CREATE OR REPLACE TABLE dim_sellers AS
SELECT DISTINCT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM sellers;
""")

# ==============================
# 7. Export tables
# ==============================
tables = [
    "fact_orders",
    "fact_order_items",
    "fact_payments",
    "dim_customers",
    "dim_products",
    "dim_sellers"
]

for table in tables:
    csv_path = PROCESSED_DIR / f"{table}.csv"
    parquet_path = PROCESSED_DIR / f"{table}.parquet"

    conn.execute(f"""
    COPY {table}
    TO '{csv_path.as_posix()}'
    WITH (HEADER, DELIMITER ',');
    """)

    conn.execute(f"""
    COPY {table}
    TO '{parquet_path.as_posix()}'
    (FORMAT PARQUET);
    """)

    row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table} created. Rows: {row_count}")

conn.close()

print("Star schema tables created successfully.")