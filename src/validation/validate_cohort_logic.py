import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

# 1. 檢查總客戶、總訂單、回購客戶數
q1 = """
WITH customer_order_count AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_orders
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
)
SELECT
    COUNT(*) AS total_customers,
    SUM(order_count) AS total_orders,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS repeat_customer_rate
FROM customer_order_count
"""

print("\n=== Repeat Customer Validation ===")
print(conn.execute(q1).fetchdf())


# 2. 檢查每個客戶購買次數分布
q2 = """
WITH customer_order_count AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_orders
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
)
SELECT
    order_count,
    COUNT(*) AS customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS customer_pct
FROM customer_order_count
GROUP BY order_count
ORDER BY order_count
"""

print("\n=== Order Count Distribution ===")
print(conn.execute(q2).fetchdf())


# 3. 檢查 cohort_index 是否合理
q3 = """
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
        co.order_id,
        fp.cohort_month,
        co.order_month,
        DATE_DIFF('month', fp.cohort_month, co.order_month) AS cohort_index
    FROM customer_orders co
    JOIN first_purchase fp
        ON co.customer_unique_id = fp.customer_unique_id
)

SELECT
    cohort_index,
    COUNT(DISTINCT customer_unique_id) AS customers,
    COUNT(DISTINCT order_id) AS orders
FROM cohort_data
GROUP BY cohort_index
ORDER BY cohort_index
"""

print("\n=== Cohort Index Distribution ===")
print(conn.execute(q3).fetchdf())


# 4. 抽幾個有回購的客戶，看日期是否正確
q4 = """
WITH customer_order_count AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM fact_orders
    WHERE customer_unique_id IS NOT NULL
    GROUP BY customer_unique_id
    HAVING COUNT(DISTINCT order_id) > 1
)

SELECT
    fo.customer_unique_id,
    fo.order_id,
    fo.order_purchase_timestamp
FROM fact_orders fo
JOIN customer_order_count coc
    ON fo.customer_unique_id = coc.customer_unique_id
ORDER BY fo.customer_unique_id, fo.order_purchase_timestamp
LIMIT 30
"""

print("\n=== Sample Repeat Customers ===")
print(conn.execute(q4).fetchdf())

conn.close()