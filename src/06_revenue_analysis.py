import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    DATE_TRUNC('month', fo.order_purchase_timestamp) AS month,
    ROUND(SUM(fp.payment_value),2) AS revenue,
    COUNT(DISTINCT fo.order_id) AS orders
FROM fact_orders fo
JOIN fact_payments fp
    ON fo.order_id = fp.order_id
GROUP BY 1
ORDER BY 1
"""

df = conn.execute(query).fetchdf()

print(df.head())

df.to_csv(
    BASE_DIR / "outputs" / "tables" / "monthly_revenue.csv",
    index=False
)

conn.close()