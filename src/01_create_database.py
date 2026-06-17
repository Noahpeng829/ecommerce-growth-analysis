import duckdb
from pathlib import Path

# ==============================
# 1. Path setting
# ==============================
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

# ==============================
# 2. Connect DuckDB
# ==============================
conn = duckdb.connect(str(DB_PATH))

# ==============================
# 3. CSV file mapping
# ==============================
tables = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv"
}

# ==============================
# 4. Create tables
# ==============================
for table_name, file_name in tables.items():
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        print(f"File not found: {file_path}")
        continue

    conn.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{file_path.as_posix()}', header=True)
    """)

    row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Created table: {table_name}, rows: {row_count}")

# ==============================
# 5. Check all tables
# ==============================
print("\nTables in database:")
print(conn.execute("SHOW TABLES").fetchdf())

conn.close()
print("\nDuckDB database created successfully.")