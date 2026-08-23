"""
generate_data.py
-----------------
Creates a small, reproducible, REAL (on-disk) dataset that the Streamlit
dashboard analyses. Task Brief requires the story to be "demonstrable live
on real (even if small) data, not just described" -- so instead of hard-
coding conclusions, this script generates transaction-level data with a
genuine, discoverable pattern baked into the mechanics (a stockout event),
and the dashboard (app.py) discovers that pattern using pandas/numpy, the
same way it would on a real company export.

Run:  python generate_data.py
Output: sales_data.csv  (~5,400 rows, Jul-Dec 2026, 4 regions x 5 categories)
"""

import numpy as np
import pandas as pd

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Beauty", "Sports"]

BASE_DAILY_UNITS = {
    "Electronics": 14, "Apparel": 20, "Home & Kitchen": 12,
    "Beauty": 16, "Sports": 10,
}
BASE_PRICE = {
    "Electronics": 3200, "Apparel": 900, "Home & Kitchen": 1500,
    "Beauty": 650, "Sports": 1100,
}
REGION_WEIGHT = {"North": 1.05, "South": 0.95, "East": 1.0, "West": 1.1}

dates = pd.date_range("2026-07-01", "2026-12-31", freq="D")

# The planted, discoverable root cause: West region ran out of Electronics
# stock for 24 days in Nov-Dec because a replenishment order was delayed.
STOCKOUT_REGION = "West"
STOCKOUT_CATEGORY = "Electronics"
STOCKOUT_START = pd.Timestamp("2026-11-10")
STOCKOUT_END = pd.Timestamp("2026-12-03")

rows = []
for d in dates:
    weekday_boost = 1.15 if d.dayofweek >= 5 else 1.0          # weekend lift
    festive_boost = 1.35 if pd.Timestamp("2026-10-15") <= d <= pd.Timestamp("2026-10-25") else 1.0  # festive sale
    for region in REGIONS:
        for cat in CATEGORIES:
            in_stockout = (
                region == STOCKOUT_REGION
                and cat == STOCKOUT_CATEGORY
                and STOCKOUT_START <= d <= STOCKOUT_END
            )
            expected_units = (
                BASE_DAILY_UNITS[cat]
                * REGION_WEIGHT[region]
                * weekday_boost
                * festive_boost
            )
            noisy_units = max(0, rng.poisson(expected_units))
            units = 0 if in_stockout else noisy_units
            price = BASE_PRICE[cat] * rng.normal(1.0, 0.04)
            marketing_spend = round(
                rng.normal(500 if cat == "Electronics" else 300, 60), 2
            )
            revenue = round(units * price, 2)
            rows.append(
                {
                    "date": d.date().isoformat(),
                    "region": region,
                    "category": cat,
                    "units_sold": units,
                    "unit_price": round(price, 2),
                    "revenue": revenue,
                    "marketing_spend": max(0, marketing_spend),
                    "stockout_flag": in_stockout,
                }
            )

df = pd.DataFrame(rows)
df.to_csv("sales_data.csv", index=False)
print(f"Wrote sales_data.csv with {len(df):,} rows")
print(df.groupby(["region", "category"])["revenue"].sum().sort_values().head())
