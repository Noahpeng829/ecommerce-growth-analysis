import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT

    is_delayed,

    COUNT(*) AS orders,

    ROUND(
        AVG(review_score),
        2
    ) AS avg_review,

    ROUND(
        AVG(actual_delivery_days),
        2
    ) AS avg_delivery_days

FROM fact_orders

WHERE review_score IS NOT NULL
  AND is_delayed IS NOT NULL
  
GROUP BY is_delayed

ORDER BY is_delayed
"""

df = conn.execute(query).fetchdf()

print(df)

output_path = (
    BASE_DIR
    / "outputs"
    / "tables"
    / "delivery_review_analysis.csv"
)

df.to_csv(output_path, index=False)

conn.close()