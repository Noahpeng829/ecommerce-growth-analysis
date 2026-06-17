import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

# ==============================
# Total Orders
# ==============================
total_orders = conn.execute("""
SELECT COUNT(DISTINCT order_id)
FROM fact_orders
""").fetchone()[0]

# ==============================
# Total Customers
# ==============================
total_customers = conn.execute("""
SELECT COUNT(DISTINCT customer_unique_id)
FROM fact_orders
""").fetchone()[0]

# ==============================
# Total Revenue
# ==============================
total_revenue = conn.execute("""
SELECT ROUND(SUM(payment_value),2)
FROM fact_payments
""").fetchone()[0]

# ==============================
# Average Order Value
# ==============================
aov = total_revenue / total_orders

# ==============================
# Average Review Score
# ==============================
avg_review = conn.execute("""
SELECT ROUND(AVG(review_score),2)
FROM fact_orders
""").fetchone()[0]

# ==============================
# Delivery Delay Rate
# ==============================
delay_rate = conn.execute("""
SELECT ROUND(AVG(is_delayed)*100,2)
FROM fact_orders
WHERE is_delayed IS NOT NULL
""").fetchone()[0]

print("="*50)
print("OLIST KPI SUMMARY")
print("="*50)

print(f"Total Orders      : {total_orders:,}")
print(f"Total Customers   : {total_customers:,}")
print(f"Total Revenue     : ${total_revenue:,.2f}")
print(f"AOV               : ${aov:,.2f}")
print(f"Avg Review Score  : {avg_review}")
print(f"Delay Rate        : {delay_rate}%")

conn.close()