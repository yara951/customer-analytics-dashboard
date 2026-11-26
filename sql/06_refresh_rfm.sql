-- Refresh customer RFM segmentation

DELETE FROM public.customer_rfm;

INSERT INTO public.customer_rfm (
    customerid,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    rfm_code,
    rfm_total_score,
    segment
)

WITH reference_date AS (
    SELECT MAX(sale_date) + 1 AS snapshot_date
    FROM public.fact_sales
),

rfm AS (
    SELECT
        customerid,
        (SELECT snapshot_date FROM reference_date)
            - MAX(sale_date) AS recency_days,
        COUNT(DISTINCT invoiceno) AS frequency,
        ROUND(SUM(revenue)::numeric, 2) AS monetary
    FROM public.fact_sales
    WHERE customerid <> -1
      AND customerid IS NOT NULL
    GROUP BY customerid
),

scores AS (
    SELECT
        *,
        CEIL(
            CUME_DIST() OVER (ORDER BY recency_days DESC) * 5
        )::int AS r_score,

        CEIL(
            CUME_DIST() OVER (ORDER BY frequency ASC) * 5
        )::int AS f_score,

        CEIL(
            CUME_DIST() OVER (ORDER BY monetary ASC) * 5
        )::int AS m_score
    FROM rfm
)

SELECT
    customerid,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) AS rfm_code,
    r_score + f_score + m_score AS rfm_total_score,

    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4
            THEN 'Champions'

        WHEN r_score <= 2 AND (f_score >= 4 OR m_score >= 4)
            THEN 'At Risk'

        WHEN r_score >= 3 AND f_score >= 4
            THEN 'Loyal Customers'

        WHEN r_score >= 4 AND f_score <= 3
            THEN 'Potential Loyalists'

        WHEN r_score <= 2 AND f_score <= 3
            THEN 'Lost Customers'

        ELSE 'Regular Customers'
    END AS segment

FROM scores;