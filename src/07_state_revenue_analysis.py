import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    dc.customer_state,
    ROUND(SUM(fp.payment_value),2) AS revenue,
    COUNT(DISTINCT fo.order_id) AS orders,
    COUNT(DISTINCT fo.customer_unique_id) AS customers,
    ROUND(
        SUM(fp.payment_value)
        /
        COUNT(DISTINCT fo.order_id),
        2
    ) AS aov

FROM fact_orders fo

JOIN dim_customers dc
    ON fo.customer_id = dc.customer_id

JOIN fact_payments fp
    ON fo.order_id = fp.order_id

GROUP BY dc.customer_state

ORDER BY revenue DESC
"""

df = conn.execute(query).fetchdf()

print(df.head(20))

output_path = (
    BASE_DIR
    / "outputs"
    / "tables"
    / "state_revenue_analysis.csv"
)

df.to_csv(output_path, index=False)

conn.close()

print(f"Saved: {output_path}")