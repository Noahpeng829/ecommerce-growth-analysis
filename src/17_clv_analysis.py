import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

query = """
WITH customer_metrics AS (
    SELECT
        fo.customer_unique_id,
        COUNT(DISTINCT fo.order_id) AS total_orders,
        ROUND(SUM(fp.payment_value), 2) AS total_revenue,
        ROUND(SUM(fp.payment_value) / COUNT(DISTINCT fo.order_id), 2) AS avg_order_value
    FROM fact_orders fo
    JOIN fact_payments fp
        ON fo.order_id = fp.order_id
    WHERE fo.customer_unique_id IS NOT NULL
    GROUP BY fo.customer_unique_id
),

clv_calc AS (
    SELECT
        customer_unique_id,
        total_orders,
        total_revenue,
        avg_order_value,
        total_revenue AS estimated_clv
    FROM customer_metrics
)

SELECT *
FROM clv_calc
ORDER BY estimated_clv DESC
"""

df = conn.execute(query).fetchdf()

output_path = OUTPUT_DIR / "customer_clv.csv"
df.to_csv(output_path, index=False)

summary_query = """
WITH customer_metrics AS (
    SELECT
        fo.customer_unique_id,
        COUNT(DISTINCT fo.order_id) AS total_orders,
        ROUND(SUM(fp.payment_value), 2) AS total_revenue,
        ROUND(SUM(fp.payment_value) / COUNT(DISTINCT fo.order_id), 2) AS avg_order_value
    FROM fact_orders fo
    JOIN fact_payments fp
        ON fo.order_id = fp.order_id
    WHERE fo.customer_unique_id IS NOT NULL
    GROUP BY fo.customer_unique_id
)

SELECT
    COUNT(*) AS customers,
    ROUND(AVG(total_revenue), 2) AS avg_clv,
    ROUND(MIN(total_revenue), 2) AS min_clv,
    ROUND(MAX(total_revenue), 2) AS max_clv,
    ROUND(
        PERCENTILE_CONT(0.5)
        WITHIN GROUP (ORDER BY total_revenue),
        2
    ) AS median_clv
FROM customer_metrics
"""

summary = conn.execute(summary_query).fetchdf()

print("=" * 60)
print("CLV Analysis")
print("=" * 60)

print("\nTop 20 Customers:")
print(df.head(20))

print("\nCLV Summary:")
print(summary)

print(f"\nSaved customer CLV to: {output_path}")

conn.close()