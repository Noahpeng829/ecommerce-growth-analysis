import duckdb
from pathlib import Path

# ==============================
# 1. Path setting
# ==============================
BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

# ==============================
# 2. Create master order table
# ==============================
query = """
CREATE OR REPLACE TABLE master_order_table AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    o.order_status,
    CAST(o.order_purchase_timestamp AS TIMESTAMP) AS order_purchase_timestamp,
    CAST(o.order_approved_at AS TIMESTAMP) AS order_approved_at,
    CAST(o.order_delivered_carrier_date AS TIMESTAMP) AS order_delivered_carrier_date,
    CAST(o.order_delivered_customer_date AS TIMESTAMP) AS order_delivered_customer_date,
    CAST(o.order_estimated_delivery_date AS TIMESTAMP) AS order_estimated_delivery_date,

    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,

    p.product_category_name,
    pct.product_category_name_english,

    s.seller_city,
    s.seller_state,

    r.review_score,

    pay.payment_type,
    pay.payment_installments,
    pay.payment_value,

    DATE_DIFF(
        'day',
        CAST(o.order_purchase_timestamp AS TIMESTAMP),
        CAST(o.order_delivered_customer_date AS TIMESTAMP)
    ) AS actual_delivery_days,

    DATE_DIFF(
        'day',
        CAST(o.order_purchase_timestamp AS TIMESTAMP),
        CAST(o.order_estimated_delivery_date AS TIMESTAMP)
    ) AS estimated_delivery_days,

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

    EXTRACT(year FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_year,
    EXTRACT(month FROM CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
    DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month_date

FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
LEFT JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct
    ON p.product_category_name = pct.product_category_name
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
LEFT JOIN order_reviews r
    ON o.order_id = r.order_id
LEFT JOIN order_payments pay
    ON o.order_id = pay.order_id
WHERE o.order_status = 'delivered';
"""

conn.execute(query)

# ==============================
# 3. Export to CSV and Parquet
# ==============================
csv_path = PROCESSED_DIR / "master_order_table.csv"
parquet_path = PROCESSED_DIR / "master_order_table.parquet"

conn.execute(f"""
COPY master_order_table
TO '{csv_path.as_posix()}'
WITH (HEADER, DELIMITER ',');
""")

conn.execute(f"""
COPY master_order_table
TO '{parquet_path.as_posix()}'
(FORMAT PARQUET);
""")

# ==============================
# 4. Basic validation
# ==============================
row_count = conn.execute("SELECT COUNT(*) FROM master_order_table").fetchone()[0]
order_count = conn.execute("SELECT COUNT(DISTINCT order_id) FROM master_order_table").fetchone()[0]
customer_count = conn.execute("SELECT COUNT(DISTINCT customer_unique_id) FROM master_order_table").fetchone()[0]

print("Master table created successfully.")
print(f"Rows: {row_count}")
print(f"Distinct orders: {order_count}")
print(f"Distinct customers: {customer_count}")
print(f"CSV exported to: {csv_path}")
print(f"Parquet exported to: {parquet_path}")

conn.close()