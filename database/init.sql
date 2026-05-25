CREATE TABLE IF NOT EXISTS currency_rates (
    rate_date DATE PRIMARY KEY,
    usd_to_eur NUMERIC(10, 4),
    gbp_to_eur NUMERIC(10, 4)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE,
    product_category VARCHAR(100) NOT NULL,
    local_currency VARCHAR(10) NOT NULL,
    price_local_currency NUMERIC(12, 2) NOT NULL,
    quantity INT NOT NULL,
    country VARCHAR(100) NOT NULL,
    order_status VARCHAR(20) NOT NULL 
);