import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

tables = [
    "fact_orders",
    "fact_order_items",
    "fact_payments"
]

print("="*60)
print("FACT TABLE VALIDATION")
print("="*60)

for table in tables:

    print(f"\n{table}")

    query = f"""
    SELECT
        COUNT(*) AS total_rows,
        COUNT(DISTINCT order_id) AS distinct_orders
    FROM {table}
    """

    print(conn.execute(query).fetchdf())

print("\nDuplicate Order Check")

for table in tables:

    query = f"""
    SELECT
        COUNT(*) AS duplicate_orders
    FROM (
        SELECT
            order_id,
            COUNT(*) AS cnt
        FROM {table}
        GROUP BY order_id
        HAVING COUNT(*) > 1
    )
    """

    result = conn.execute(query).fetchone()[0]

    print(
        f"{table}: {result}"
    )

conn.close()