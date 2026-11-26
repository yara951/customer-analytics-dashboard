-- Refresh the main retail sales table

DELETE FROM public.retail_sales;

INSERT INTO public.retail_sales (
    invoiceno,
    stockcode,
    description,
    quantity,
    invoicedate,
    unitprice,
    customerid,
    country,
    iscancellation,
    invalidquantity,
    invalidprice,
    invaliddate,
    revenue
)
SELECT
    invoiceno,
    stockcode,
    description,
    quantity,
    invoicedate,
    unitprice,
    customerid,
    country,
    iscancellation,
    invalidquantity,
    invalidprice,
    invaliddate,
    revenue
FROM public.retail_sales_staging;