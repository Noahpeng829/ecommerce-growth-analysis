import duckdb
from pathlib import Path

print("Running customer value distribution script...")

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

query = """
WITH distinct_orders AS (
    SELECT DISTINCT
        order_id,
        customer_unique_id
    FROM fact_orders
    WHERE customer_unique_id IS NOT NULL
),

order_payments AS (
    SELECT
        order_id,
        SUM(payment_value) AS order_revenue
    FROM fact_payments
    GROUP BY order_id
),

customer_revenue AS (
    SELECT
        d.customer_unique_id,
        SUM(op.order_revenue) AS total_revenue
    FROM distinct_orders d
    JOIN order_payments op
        ON d.order_id = op.order_id
    GROUP BY d.customer_unique_id
),

ranked_customers AS (
    SELECT
        customer_unique_id,
        total_revenue,
        NTILE(100) OVER (
            ORDER BY total_revenue DESC
        ) AS revenue_percentile
    FROM customer_revenue
)

SELECT
    revenue_percentile,
    COUNT(*) AS customers,
    ROUND(SUM(total_revenue), 2) AS revenue
FROM ranked_customers
GROUP BY revenue_percentile
ORDER BY revenue_percentile
"""

df = conn.execute(query).fetchdf()

output_path = OUTPUT_DIR / "customer_value_distribution.csv"
df.to_csv(output_path, index=False)

total_revenue = df["revenue"].sum()
top10 = df[df["revenue_percentile"] <= 10]["revenue"].sum()
top20 = df[df["revenue_percentile"] <= 20]["revenue"].sum()

print("=" * 60)
print("Customer Value Distribution")
print("=" * 60)

print(f"\nTotal Revenue: ${total_revenue:,.2f}")
print(f"\nTop 10% Customers Revenue Share: {top10 / total_revenue * 100:.2f}%")
print(f"Top 20% Customers Revenue Share: {top20 / total_revenue * 100:.2f}%")

print("\nTop 20 Percentiles")
print(df.head(20))

print(f"\nSaved to: {output_path}")

conn.close()