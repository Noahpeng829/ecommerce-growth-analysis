import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT

    dp.product_category_name_english AS category,

    COUNT(*) AS items_sold,

    ROUND(
        AVG(fo.delivery_delay_days),
        2
    ) AS avg_delay_days,

    ROUND(
        AVG(fo.review_score),
        2
    ) AS avg_review,

    ROUND(
        SUM(foi.price),
        2
    ) AS revenue

FROM fact_order_items foi

JOIN dim_products dp
    ON foi.product_id = dp.product_id

JOIN fact_orders fo
    ON foi.order_id = fo.order_id

WHERE fo.review_score IS NOT NULL

GROUP BY category

HAVING COUNT(*) >= 100

ORDER BY avg_delay_days DESC
"""

df = conn.execute(query).fetchdf()

print(df.head(30))

conn.close()