-- Vérifier le nombre de lignes
SELECT COUNT(*) AS total_rows
FROM retail_sales;

-- Vérifier les clients anonymes
SELECT COUNT(*) AS anonymous_sales
FROM retail_sales
WHERE customerid IS NULL;

-- Vérifier les dates
SELECT
    MIN(invoicedate) AS first_date,
    MAX(invoicedate) AS last_date
FROM retail_sales;