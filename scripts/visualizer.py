import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

print("Starting visualization...")

DATABASE_URL = "postgresql+pg8000://analyst:market_analytics_2026@localhost:5432/zalando_db"
engine = create_engine(DATABASE_URL)

query = """
SELECT 
    o.order_id,
    o.order_date,
    o.product_category,
    o.country,
    o.order_status,
    o.quantity,
    CASE 
        WHEN o.local_currency = 'EUR' THEN o.price_local_currency
        WHEN o.local_currency = 'USD' THEN o.price_local_currency * c.usd_to_eur
        WHEN o.local_currency = 'GBP' THEN o.price_local_currency * c.gbp_to_eur
        WHEN o.local_currency = 'AMD' THEN o.price_local_currency * 0.0024
        ELSE o.price_local_currency
    END as price_eur
FROM orders o
LEFT JOIN currency_rates c ON o.order_date::DATE = c.rate_date
"""

try:
    df = pd.read_sql(query, engine)
    df['total_revenue_eur'] = df['price_eur'] * df['quantity']
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    sns.barplot(
        data=df, 
        x='product_category', 
        y='total_revenue_eur', 
        hue='order_status', 
        estimator=sum, 
        errorbar=None
    )
    
    plt.title('Market Revenue and Returns by Category (EUR)')
    plt.xlabel('Category')
    plt.ylabel('Total Sales (EUR)')
    plt.legend(title='Status')
    plt.tight_layout()
    
    output_path = "data/market_analytics_chart.png"
    plt.savefig(output_path)
    print(f"Chart saved to {output_path}")
    print("Visualization finished successfully.")
    
except Exception as e:
    print(f"Visualization failed: {e}")