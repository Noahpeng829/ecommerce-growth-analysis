import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    ROUND(SUM(price),2) AS product_revenue,
    ROUND(SUM(freight_value),2) AS freight_revenue,
    ROUND(SUM(price + freight_value),2) AS total_item_value
FROM fact_order_items
"""

result = conn.execute(query).fetchdf()

print(result)

conn.close()