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
        SUM(foi.price),
        2
    ) AS product_revenue,

    ROUND(
        AVG(foi.price),
        2
    ) AS avg_item_price

FROM fact_order_items foi

JOIN dim_products dp
    ON foi.product_id = dp.product_id

GROUP BY category

ORDER BY product_revenue DESC
LIMIT 20
"""

df = conn.execute(query).fetchdf()

print(df)

output_path = (
    BASE_DIR
    / "outputs"
    / "tables"
    / "top_category_revenue.csv"
)

df.to_csv(output_path, index=False)

conn.close()