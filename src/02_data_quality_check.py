import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

tables = [
    "customers",
    "geolocation",
    "order_items",
    "order_payments",
    "order_reviews",
    "orders",
    "products",
    "sellers",
    "product_category_translation"
]

# ==================================================
# 1. Table-level summary
# ==================================================

table_summary = []

for table in tables:
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    col_info = conn.execute(f"DESCRIBE {table}").fetchdf()
    col_count = len(col_info)

    table_summary.append({
        "table_name": table,
        "row_count": row_count,
        "column_count": col_count
    })

table_summary_df = pd.DataFrame(table_summary)
table_summary_df.to_csv(
    OUTPUT_DIR / "data_quality_table_summary.csv",
    index=False
)

print("\n=== Table Summary ===")
print(table_summary_df)


# ==================================================
# 2. Column-level missing values + unique values
# ==================================================

column_quality = []

for table in tables:
    row_count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    columns = conn.execute(f"DESCRIBE {table}").fetchdf()

    for _, row in columns.iterrows():
        column_name = row["column_name"]
        data_type = row["column_type"]

        missing_count = conn.execute(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE "{column_name}" IS NULL
        """).fetchone()[0]

        unique_count = conn.execute(f"""
            SELECT COUNT(DISTINCT "{column_name}")
            FROM {table}
        """).fetchone()[0]

        missing_pct = round(missing_count / row_count * 100, 2)

        column_quality.append({
            "table_name": table,
            "column_name": column_name,
            "data_type": data_type,
            "row_count": row_count,
            "missing_count": missing_count,
            "missing_pct": missing_pct,
            "unique_count": unique_count
        })

column_quality_df = pd.DataFrame(column_quality)
column_quality_df.to_csv(
    OUTPUT_DIR / "data_quality_column_profile.csv",
    index=False
)

print("\n=== Column Quality Profile ===")
print(column_quality_df.head(30))


# ==================================================
# 3. Primary key duplicate checks
# ==================================================

key_checks = [
    ("customers", "customer_id"),
    ("customers", "customer_unique_id"),
    ("orders", "order_id"),
    ("products", "product_id"),
    ("sellers", "seller_id"),
]

duplicate_results = []

for table, key in key_checks:
    result = conn.execute(f"""
        SELECT
            COUNT(*) AS row_count,
            COUNT(DISTINCT "{key}") AS unique_key_count,
            COUNT(*) - COUNT(DISTINCT "{key}") AS duplicate_count
        FROM {table}
    """).fetchdf()

    duplicate_results.append({
        "table_name": table,
        "key_column": key,
        "row_count": int(result.loc[0, "row_count"]),
        "unique_key_count": int(result.loc[0, "unique_key_count"]),
        "duplicate_count": int(result.loc[0, "duplicate_count"])
    })

duplicate_df = pd.DataFrame(duplicate_results)
duplicate_df.to_csv(
    OUTPUT_DIR / "data_quality_duplicate_check.csv",
    index=False
)

print("\n=== Duplicate Key Check ===")
print(duplicate_df)


# ==================================================
# 4. Business rule checks
# ==================================================

business_checks = []

# Delivered orders should have delivered customer date
delivered_missing_date = conn.execute("""
    SELECT COUNT(*)
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NULL
""").fetchone()[0]

business_checks.append({
    "check_name": "Delivered orders with missing delivered_customer_date",
    "issue_count": delivered_missing_date
})

# Orders with missing purchase timestamp
missing_purchase_date = conn.execute("""
    SELECT COUNT(*)
    FROM orders
    WHERE order_purchase_timestamp IS NULL
""").fetchone()[0]

business_checks.append({
    "check_name": "Orders with missing purchase timestamp",
    "issue_count": missing_purchase_date
})

# Products without English category after translation
missing_english_category = conn.execute("""
    SELECT COUNT(*)
    FROM products p
    LEFT JOIN product_category_translation pct
        ON p.product_category_name = pct.product_category_name
    WHERE pct.product_category_name_english IS NULL
""").fetchone()[0]

business_checks.append({
    "check_name": "Products without English category mapping",
    "issue_count": missing_english_category
})

# Order items with missing price
missing_price = conn.execute("""
    SELECT COUNT(*)
    FROM order_items
    WHERE price IS NULL
""").fetchone()[0]

business_checks.append({
    "check_name": "Order items with missing price",
    "issue_count": missing_price
})

# Payments with missing payment value
missing_payment_value = conn.execute("""
    SELECT COUNT(*)
    FROM order_payments
    WHERE payment_value IS NULL
""").fetchone()[0]

business_checks.append({
    "check_name": "Payments with missing payment value",
    "issue_count": missing_payment_value
})

business_df = pd.DataFrame(business_checks)
business_df.to_csv(
    OUTPUT_DIR / "data_quality_business_rules.csv",
    index=False
)

print("\n=== Business Rule Check ===")
print(business_df)


conn.close()

print("\nData quality check completed.")