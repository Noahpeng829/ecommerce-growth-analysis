import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect()

query = """
WITH customer_revenue AS (
    SELECT
        customer_unique_id,
        total_revenue
    FROM read_csv_auto('outputs/tables/customer_clv.csv')
),

rfm AS (
    SELECT
        customer_unique_id,
        customer_segment
    FROM read_csv_auto('outputs/tables/rfm_customer_segments.csv')
)

SELECT
    r.customer_segment,
    COUNT(*) AS customers,
    ROUND(SUM(cr.total_revenue), 2) AS revenue,
    ROUND(AVG(cr.total_revenue), 2) AS avg_customer_revenue
FROM rfm r
JOIN customer_revenue cr
    ON r.customer_unique_id = cr.customer_unique_id
GROUP BY r.customer_segment
ORDER BY revenue DESC

"""

df = conn.execute(query).fetchdf()

output_path = OUTPUT_DIR / "segment_revenue_contribution.csv"

df.to_csv(output_path, index=False)

print("=" * 60)
print("Segment Revenue Contribution")
print("=" * 60)
print(df)

print(f"\nSaved to: {output_path}")

conn.close()