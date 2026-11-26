-- ONLINE RETAIL - DATABASE SETUP
-- Run in an existing PostgreSQL database before running the ETL pipeline.
-- Creates the core warehouse objects; does not load data or drop tables.

BEGIN;

-- 1. Physical tables
CREATE TABLE IF NOT EXISTS public.retail_sales (
    invoiceno TEXT,
    stockcode TEXT,
    description TEXT,
    quantity BIGINT,
    invoicedate TIMESTAMP WITHOUT TIME ZONE,
    unitprice DOUBLE PRECISION,
    customerid BIGINT,
    country TEXT,
    iscancellation BOOLEAN,
    invalidquantity BOOLEAN,
    invalidprice BOOLEAN,
    invaliddate BOOLEAN,
    revenue DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS public.customer_rfm (
    customerid BIGINT,
    recency_days BIGINT,
    frequency BIGINT,
    monetary DOUBLE PRECISION,
    r_score BIGINT,
    f_score BIGINT,
    m_score BIGINT,
    rfm_code TEXT,
    rfm_total_score BIGINT,
    segment TEXT
);

-- 2. Country dimension
CREATE OR REPLACE VIEW public.dim_country AS
SELECT DISTINCT TRIM(country) AS country
FROM public.retail_sales
WHERE country IS NOT NULL AND TRIM(country) <> '';

-- 3. Customer dimension (unknown customer = -1)
CREATE OR REPLACE VIEW public.dim_customer AS
SELECT DISTINCT customerid
FROM public.retail_sales
WHERE customerid IS NOT NULL
UNION ALL
SELECT -1::bigint AS customerid;

-- 4. Date dimension
CREATE OR REPLACE VIEW public.dim_date AS
SELECT d::date AS date,
    EXTRACT(YEAR FROM d)::integer AS year,
    EXTRACT(QUARTER FROM d)::integer AS quarter,
    EXTRACT(MONTH FROM d)::integer AS month,
    TO_CHAR(d, 'FMMonth') AS month_name,
    EXTRACT(DAY FROM d)::integer AS day,
    TO_CHAR(d, 'FMDay') AS day_name
FROM generate_series(
    (SELECT MIN(invoicedate)::date FROM public.retail_sales)::timestamptz,
    (SELECT MAX(invoicedate)::date FROM public.retail_sales)::timestamptz,
    INTERVAL '1 day'
) AS dates(d);

-- 5. Product dimension
CREATE OR REPLACE VIEW public.dim_product AS
WITH description_counts AS (
    SELECT UPPER(TRIM(stockcode)) AS stockcode,
        description, COUNT(*) AS occurrences
    FROM public.retail_sales
    WHERE stockcode IS NOT NULL AND TRIM(stockcode) <> ''
    GROUP BY UPPER(TRIM(stockcode)), description
), ranked_descriptions AS (
    SELECT stockcode, description,
        ROW_NUMBER() OVER (
            PARTITION BY stockcode
            ORDER BY CASE WHEN description IS NULL OR TRIM(description) = ''
                          THEN 1 ELSE 0 END,
                     occurrences DESC, description ASC
        ) AS rn
    FROM description_counts
)
SELECT stockcode,
    COALESCE(NULLIF(TRIM(description), ''), 'Unknown') AS product_name,
    CASE
        WHEN stockcode IN ('POST', 'DOT', 'C2') THEN 'Shipping'
        WHEN stockcode IN ('AMAZONFEE', 'BANK CHARGES') THEN 'Fee'
        WHEN stockcode ~ '^GIFT_' THEN 'Gift Card'
        WHEN stockcode = 'M' THEN 'Manual'
        WHEN stockcode = 'B' THEN 'Adjustment'
        WHEN stockcode = 'S' THEN 'Sample'
        WHEN stockcode ~ '^[0-9]{5}[A-Z]{0,2}$'
             OR stockcode LIKE 'DCGS%' OR stockcode = 'PADS' THEN 'Product'
        ELSE 'Other'
    END AS product_type
FROM ranked_descriptions
WHERE rn = 1;

-- 6. Sales fact view
CREATE OR REPLACE VIEW public.fact_sales AS
SELECT invoiceno,
    UPPER(TRIM(stockcode)) AS stockcode,
    COALESCE(customerid, -1::bigint) AS customerid,
    TRIM(country) AS country,
    invoicedate::date AS sale_date,
    quantity, unitprice, revenue
FROM public.retail_sales;

COMMIT;

-- retail_sales_staging is created by src/load.py.
-- Next: configure .env and run python -m src.pipeline from the project root.
