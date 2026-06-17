import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    order_id,
    COUNT(*) AS review_count
FROM order_reviews
GROUP BY order_id
HAVING COUNT(*) > 1
ORDER BY review_count DESC
LIMIT 20
"""

print(conn.execute(query).fetchdf())

conn.close()    