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
        fo.customer_unique_id,
        fo.order_id,
        fo.order_purchase_timestamp,
        SUM(fp.payment_value) AS order_value
    FROM fact_orders fo
    JOIN fact_payments fp
        ON fo.order_id = fp.order_id
    WHERE fo.customer_unique_id IS NOT NULL
    GROUP BY
        fo.customer_unique_id,
        fo.order_id,
        fo.order_purchase_timestamp
),

reference_date AS (
    SELECT
        MAX(order_purchase_timestamp) + INTERVAL 1 DAY AS ref_date
    FROM customer_orders
),

rfm_base AS (
    SELECT
        co.customer_unique_id,

        DATE_DIFF(
            'day',
            MAX(co.order_purchase_timestamp),
            (SELECT ref_date FROM reference_date)
        ) AS recency,

        COUNT(DISTINCT co.order_id) AS frequency,

        ROUND(SUM(co.order_value), 2) AS monetary

    FROM customer_orders co
    GROUP BY co.customer_unique_id
),

rfm_scores AS (
    SELECT
        customer_unique_id,
        recency,
        frequency,
        monetary,

        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score

    FROM rfm_base
),

rfm_segment AS (
    SELECT
        customer_unique_id,
        recency,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        r_score + f_score + m_score AS rfm_score,

        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
                THEN 'Champions'
            WHEN r_score >= 4 AND f_score >= 3
                THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score <= 2
                THEN 'Recent Customers'
            WHEN r_score <= 2 AND f_score >= 4
                THEN 'At Risk'
            WHEN r_score <= 2 AND f_score <= 2
                THEN 'Lost Customers'
            WHEN m_score >= 4
                THEN 'High Value'
            ELSE 'Others'
        END AS customer_segment

    FROM rfm_scores
)

SELECT *
FROM rfm_segment
ORDER BY rfm_score DESC
"""

df = conn.execute(query).fetchdf()

output_path = OUTPUT_DIR / "rfm_customer_segments.csv"
df.to_csv(output_path, index=False)

print("=" * 60)
print("RFM Segmentation Completed")
print("=" * 60)

print("\nTop 10 Customers:")
print(df.head(10))

print("\nSegment Summary:")
segment_summary = conn.execute("""
WITH customer_orders AS (
    SELECT
        fo.customer_unique_id,
        fo.order_id,
        fo.order_purchase_timestamp,
        SUM(fp.payment_value) AS order_value
    FROM fact_orders fo
    JOIN fact_payments fp
        ON fo.order_id = fp.order_id
    WHERE fo.customer_unique_id IS NOT NULL
    GROUP BY
        fo.customer_unique_id,
        fo.order_id,
        fo.order_purchase_timestamp
),

reference_date AS (
    SELECT
        MAX(order_purchase_timestamp) + INTERVAL 1 DAY AS ref_date
    FROM customer_orders
),

rfm_base AS (
    SELECT
        co.customer_unique_id,

        DATE_DIFF(
            'day',
            MAX(co.order_purchase_timestamp),
            (SELECT ref_date FROM reference_date)
        ) AS recency,

        COUNT(DISTINCT co.order_id) AS frequency,

        ROUND(SUM(co.order_value), 2) AS monetary

    FROM customer_orders co
    GROUP BY co.customer_unique_id
),

rfm_scores AS (
    SELECT
        customer_unique_id,
        recency,
        frequency,
        monetary,

        NTILE(5) OVER (ORDER BY recency DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score

    FROM rfm_base
),

rfm_segment AS (
    SELECT
        customer_unique_id,
        recency,
        frequency,
        monetary,
        r_score,
        f_score,
        m_score,
        r_score + f_score + m_score AS rfm_score,

        CASE
            WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
                THEN 'Champions'
            WHEN r_score >= 4 AND f_score >= 3
                THEN 'Loyal Customers'
            WHEN r_score >= 4 AND f_score <= 2
                THEN 'Recent Customers'
            WHEN r_score <= 2 AND f_score >= 4
                THEN 'At Risk'
            WHEN r_score <= 2 AND f_score <= 2
                THEN 'Lost Customers'
            WHEN m_score >= 4
                THEN 'High Value'
            ELSE 'Others'
        END AS customer_segment

    FROM rfm_scores
)

SELECT
    customer_segment,
    COUNT(*) AS customers,
    ROUND(AVG(recency), 2) AS avg_recency,
    ROUND(AVG(frequency), 2) AS avg_frequency,
    ROUND(AVG(monetary), 2) AS avg_monetary,
    ROUND(SUM(monetary), 2) AS total_revenue
FROM rfm_segment
GROUP BY customer_segment
ORDER BY total_revenue DESC
""").fetchdf()

print(segment_summary)

summary_path = OUTPUT_DIR / "rfm_segment_summary.csv"
segment_summary.to_csv(summary_path, index=False)

print(f"\nSaved customer segments to: {output_path}")
print(f"Saved segment summary to: {summary_path}")

conn.close()   