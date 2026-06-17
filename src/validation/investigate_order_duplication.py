import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    order_id,
    COUNT(*) AS row_count
FROM fact_orders
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY row_count DESC
LIMIT 20
"""

print(
    conn.execute(query).fetchdf()
)

conn.close()