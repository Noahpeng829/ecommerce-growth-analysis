import duckdb
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "tables"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

# 1. Executive KPI
kpi_query = """
WITH review_dedup AS (
    SELECT
        order_id,
        AVG(review_score) AS review_score,
        MAX(is_delayed) AS is_delayed
    FROM fact_orders
    WHERE is_delayed IS NOT NULL
    GROUP BY order_id
),

order_customer AS (
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

order_level AS (
    SELECT
        oc.order_id,
        oc.customer_unique_id,
        rd.review_score,
        rd.is_delayed,
        op.order_revenue
    FROM order_customer oc
    JOIN review_dedup rd
        ON oc.order_id = rd.order_id
    JOIN order_payments op
        ON oc.order_id = op.order_id
)

SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(order_revenue), 2) AS total_revenue,
    ROUND(SUM(order_revenue) / COUNT(DISTINCT order_id), 2) AS aov,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(AVG(is_delayed) * 100, 2) AS delay_rate
FROM order_level
"""

kpi_df = conn.execute(kpi_query).fetchdf()
kpi_df.to_csv(OUTPUT_DIR / "executive_kpi_summary.csv", index=False)

# 2. Key Insights Table
insights = [
    {
        "insight_area": "Delivery Experience",
        "finding": "Delayed orders had much lower review scores than on-time orders.",
        "metric": "On-time review: 4.29; delayed review: 2.57; p-value < 0.001",
        "business_recommendation": "Prioritize delivery performance improvements to protect customer satisfaction."
    },
    {
        "insight_area": "Customer Retention",
        "finding": "Most customers purchased only once.",
        "metric": "97% of customers placed only one order; repeat customer rate: 3%",
        "business_recommendation": "Develop retention campaigns and post-purchase engagement strategies."
    },
    {
        "insight_area": "Customer Value",
        "finding": "Revenue is moderately concentrated among high-value customers.",
        "metric": "Top 20% customers contributed 53.54% of total revenue.",
        "business_recommendation": "Focus CRM efforts on high-value customers while improving repeat purchase behavior."
    },
    {
        "insight_area": "Category Risk",
        "finding": "Some high-revenue categories had below-average review scores.",
        "metric": "Office furniture review: 3.52; bed_bath_table review: 3.92",
        "business_recommendation": "Investigate product quality, delivery, and expectation mismatch in risk categories."
    }
]

insight_df = pd.DataFrame(insights)
insight_df.to_csv(OUTPUT_DIR / "executive_key_insights.csv", index=False)

print("=" * 60)
print("Executive Summary Tables Created")
print("=" * 60)

print("\nExecutive KPI Summary:")
print(kpi_df)

print("\nExecutive Key Insights:")
print(insight_df)

print("\nSaved:")
print(OUTPUT_DIR / "executive_kpi_summary.csv")
print(OUTPUT_DIR / "executive_key_insights.csv")

conn.close()