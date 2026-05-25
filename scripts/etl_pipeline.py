import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import create_engine

print("Starting ETL process...")

DATABASE_URL = "postgresql+pg8000://analyst:market_analytics_2026@localhost:5432/zalando_db"
engine = create_engine(DATABASE_URL)

print("Generating currency rates...")
dates = pd.date_range(start="2026-01-01", end="2026-05-25", freq="D")
currency_data = {
    "rate_date": dates,
    "usd_to_eur": np.random.uniform(0.91, 0.93, len(dates)),
    "gbp_to_eur": np.random.uniform(1.15, 1.18, len(dates))
}
df_currency = pd.DataFrame(currency_data)

print("Generating market transactions...")
np.random.seed(42)
n_orders = 1000

categories = ['Shoes', 'Apparel', 'Accessories', 'Premium', 'Sports']
countries = ['Germany', 'France', 'Armenia', 'United Kingdom', 'Austria', 'Netherlands']
currencies = ['EUR', 'EUR', 'AMD', 'GBP', 'EUR', 'EUR']
country_currency = dict(zip(countries, currencies))

order_dates = [datetime(2026, 1, 1) + timedelta(days=int(np.random.randint(0, 140))) for _ in range(n_orders)]

orders_data = []
for i in range(n_orders):
    o_date = order_dates[i]
    status = np.random.choice(['Completed', 'Returned'], p=[0.65, 0.35])
    del_date = o_date + timedelta(days=int(np.random.randint(2, 8)))
    country = np.random.choice(countries)
    loc_curr = country_currency[country]
    
    if loc_curr == 'AMD':
        price = round(np.random.uniform(15000, 80000), -2)
    elif loc_curr == 'GBP':
        price = round(np.random.uniform(30, 180), 2)
    else:
        price = round(np.random.uniform(40, 200), 2)
        
    orders_data.append({
        "order_id": f"MKT-{100000 + i}",
        "customer_id": f"CUST-{np.random.randint(1000, 1500)}",
        "order_date": o_date.strftime('%Y-%m-%d'),
        "delivery_date": del_date.strftime('%Y-%m-%d'),
        "product_category": np.random.choice(categories),
        "local_currency": loc_curr,
        "price_local_currency": price,
        "quantity": int(np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])),
        "country": country,
        "order_status": status
    })

df_orders = pd.DataFrame(orders_data)

print("Saving backup to CSV...")
df_orders.to_csv("data/market_orders_backup.csv", index=False)

print("Loading data to database...")
try:
    df_currency.to_sql("currency_rates", engine, if_exists="append", index=False)
    df_orders.to_sql("orders", engine, if_exists="append", index=False)
    print("ETL finished successfully.")
except Exception as e:
    print(f"ETL failed: {e}")