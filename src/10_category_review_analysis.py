import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT

    dp.product_category_name_english AS category,

    COUNT(*) AS items_sold,

    ROUND(SUM(foi.price),2) AS revenue,

    ROUND(AVG(fo.review_score),2) AS avg_review,

    ROUND(AVG(foi.price),2) AS avg_price

FROM fact_order_items foi

JOIN dim_products dp
    ON foi.product_id = dp.product_id

JOIN fact_orders fo
    ON foi.order_id = fo.order_id

WHERE fo.review_score IS NOT NULL

GROUP BY category

HAVING COUNT(*) >= 100

ORDER BY revenue DESC
"""

df = conn.execute(query).fetchdf()

print(df.head(30))

output_path = (
    BASE_DIR
    / "outputs"
    / "tables"
    / "category_review_analysis.csv"
)

df.to_csv(output_path, index=False)

conn.close()

print("Saved:", output_path)
