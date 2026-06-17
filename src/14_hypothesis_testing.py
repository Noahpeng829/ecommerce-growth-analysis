import duckdb
import pandas as pd
from scipy.stats import ttest_ind
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "olist_ecommerce.duckdb"

conn = duckdb.connect(str(DB_PATH))

query = """
SELECT
    review_score,
    is_delayed
FROM fact_orders
WHERE review_score IS NOT NULL
  AND is_delayed IS NOT NULL
"""

df = conn.execute(query).fetchdf()

conn.close()

on_time = df[df["is_delayed"] == 0]["review_score"]
delayed = df[df["is_delayed"] == 1]["review_score"]

t_stat, p_value = ttest_ind(
    on_time,
    delayed,
    equal_var=False
)

print("="*50)
print("Hypothesis Test")
print("="*50)

print(f"On-time Mean Review : {on_time.mean():.3f}")
print(f"Delayed Mean Review : {delayed.mean():.3f}")

print(f"T-statistic : {t_stat:.4f}")
print(f"P-value     : {p_value:.20f}")

if p_value < 0.05:
    print("\nReject H0")
    print("Delivery delay significantly impacts review scores.")
else:
    print("\nFail to Reject H0")