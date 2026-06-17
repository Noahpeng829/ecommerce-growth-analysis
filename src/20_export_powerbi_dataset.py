import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"
OUTPUT_DIR = BASE_DIR / "outputs" / "powerbi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(str(DB_PATH))

exports = {
    "powerbi_orders.csv": """
        SELECT
            order_id,
            customer_unique_id,
            MIN(order_purchase_timestamp) AS order_purchase_timestamp,
            MIN(order_month_date) AS order_month_date,
            AVG(actual_delivery_days) AS actual_delivery_days,
            AVG(delivery_delay_days) AS delivery_delay_days,
            MAX(is_delayed) AS is_delayed,
            AVG(review_score) AS review_score
        FROM fact_orders
        WHERE is_delayed IS NOT NULL
        GROUP BY
            order_id,
            customer_unique_id
    """,

    "powerbi_revenue.csv": """
        WITH order_payments AS (
            SELECT
                order_id,
                SUM(payment_value) AS order_revenue
            FROM fact_payments
            GROUP BY order_id
        )
        SELECT
            fo.order_id,
            fo.customer_unique_id,
            fo.order_month_date,
            op.order_revenue
        FROM (
            SELECT
                order_id,
                customer_unique_id,
                MIN(order_month_date) AS order_month_date
            FROM fact_orders
            WHERE is_delayed IS NOT NULL
            GROUP BY
                order_id,
                customer_unique_id
        ) fo
        JOIN order_payments op
            ON fo.order_id = op.order_id
    """,

    "powerbi_categories.csv": """
        SELECT
            dp.product_category_name_english AS category,
            COUNT(*) AS items_sold,
            ROUND(SUM(foi.price), 2) AS product_revenue,
            ROUND(AVG(fo.review_score), 2) AS avg_review,
            ROUND(AVG(fo.is_delayed) * 100, 2) AS delay_rate
        FROM fact_order_items foi
        JOIN dim_products dp
            ON foi.product_id = dp.product_id
        JOIN fact_orders fo
            ON foi.order_id = fo.order_id
        WHERE fo.review_score IS NOT NULL
          AND fo.is_delayed IS NOT NULL
        GROUP BY dp.product_category_name_english
    """,

    "powerbi_customers.csv": """
        SELECT
            *
        FROM read_csv_auto('outputs/tables/rfm_customer_segments.csv')
    """,

    "powerbi_cohort.csv": """
        SELECT
            *
        FROM read_csv_auto('outputs/tables/cohort_retention_long.csv')
    """,

    "powerbi_customer_value_distribution.csv": """
        SELECT
            *
        FROM read_csv_auto('outputs/tables/customer_value_distribution.csv')
    """,

    "powerbi_executive_kpi.csv": """
        SELECT
            *
        FROM read_csv_auto('outputs/tables/executive_kpi_summary.csv')
    """,

    "powerbi_key_insights.csv": """
        SELECT
            *
        FROM read_csv_auto('outputs/tables/executive_key_insights.csv')
    """,
    "powerbi_segment_revenue.csv": """
    SELECT
        *
    FROM read_csv_auto('outputs/tables/segment_revenue_contribution.csv')
    """
}

for filename, query in exports.items():
    output_path = OUTPUT_DIR / filename

    conn.execute(f"""
        COPY ({query})
        TO '{output_path.as_posix()}'
        WITH (HEADER, DELIMITER ',')
    """)

    print(f"Exported: {output_path}")

conn.close()

print("\nPower BI datasets exported successfully.")