import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

query = """
WITH customer_orders AS (
    SELECT
        customer_unique_id,
        order_id,
        DATE_TRUNC('month', order_purchase_timestamp) AS order_month
    FROM fact_orders
    WHERE customer_unique_id IS NOT NULL
),

first_purchase AS (
    SELECT
        customer_unique_id,
        MIN(order_month) AS cohort_month
    FROM customer_orders
    GROUP BY customer_unique_id
),

cohort_data AS (
    SELECT
        co.customer_unique_id,
        fp.cohort_month,
        co.order_month,

        DATE_DIFF(
            'month',
            fp.cohort_month,
            co.order_month
        ) AS cohort_index

    FROM customer_orders co
    JOIN first_purchase fp
        ON co.customer_unique_id = fp.customer_unique_id
),

cohort_counts AS (
    SELECT
        cohort_month,
        cohort_index,
        COUNT(DISTINCT customer_unique_id) AS customers
    FROM cohort_data
    GROUP BY cohort_month, cohort_index
),

cohort_size AS (
    SELECT
        cohort_month,
        customers AS cohort_size
    FROM cohort_counts
    WHERE cohort_index = 0
)

SELECT
    cc.cohort_month,
    cc.cohort_index,
    cc.customers,
    cs.cohort_size,
    ROUND(
        cc.customers * 100.0 / cs.cohort_size,
        2
    ) AS retention_rate
FROM cohort_counts cc
JOIN cohort_size cs
    ON cc.cohort_month = cs.cohort_month
ORDER BY cc.cohort_month, cc.cohort_index
"""

df = conn.execute(query).fetchdf()

# Long format
long_path = OUTPUT_DIR / "cohort_retention_long.csv"
df.to_csv(long_path, index=False)

# Pivot retention table
pivot_df = df.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="retention_rate"
).reset_index()

pivot_path = OUTPUT_DIR / "cohort_retention_pivot.csv"
pivot_df.to_csv(pivot_path, index=False)

print("=" * 60)
print("Cohort Analysis Completed")
print("=" * 60)

print("\nCohort Retention Long Format:")
print(df.head(30))

print("\nCohort Retention Pivot Table:")
print(pivot_df.head(15))

print(f"\nSaved long format to: {long_path}")
print(f"Saved pivot table to: {pivot_path}")

conn.close()