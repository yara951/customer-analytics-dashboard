import pandas as pd


def transform_data(df: pd.DataFrame):

    print("Transforming data...")
    initial_rows = len(df)

    # Remove duplicates
    df = df.drop_duplicates().copy()

    # Normalize data types
    df["InvoiceNo"] = df["InvoiceNo"].astype("string").str.strip()
    df["StockCode"] = df["StockCode"].astype("string").str.strip()

    df["CustomerID"] = pd.to_numeric(
        df["CustomerID"], errors="coerce"
    ).astype("Int64")

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"], errors="coerce"
    )

    df["Description"] = df["Description"].astype("string").str.strip()

    # Identify data quality issues
    df["IsCancellation"] = df["InvoiceNo"].str.startswith("C", na=False)

    df["InvalidQuantity"] = df["Quantity"].isna() | (df["Quantity"] <= 0)
    df["InvalidPrice"] = df["UnitPrice"].isna() | (df["UnitPrice"] <= 0)
    df["InvalidDate"] = df["InvoiceDate"].isna()

    # Generate data quality report
    quality_report = pd.DataFrame({
        "Issue": [
            "Missing CustomerID",
            "Missing Description",
            "Cancelled invoices",
            "Invalid quantities",
            "Invalid prices",
            "Invalid dates"
        ],
        "Count": [
            df["CustomerID"].isna().sum(),
            df["Description"].isna().sum(),
            df["IsCancellation"].sum(),
            df["InvalidQuantity"].sum(),
            df["InvalidPrice"].sum(),
            df["InvalidDate"].sum()
        ]
    })

    # Keep valid transactions
    valid_sales_mask = (
        ~df["IsCancellation"]
        & ~df["InvalidQuantity"]
        & ~df["InvalidPrice"]
        & ~df["InvalidDate"]
    )

    sales_clean = df.loc[valid_sales_mask].copy()

    # Calculate revenue
    sales_clean["Revenue"] = (
        sales_clean["Quantity"] * sales_clean["UnitPrice"]
    )

    # Keep identified customers
    customer_sales = sales_clean[
        sales_clean["CustomerID"].notna()
    ].copy()

    # Transformation summary
    print(f"Initial rows: {initial_rows:,}")
    print(f"Clean sales: {len(sales_clean):,}")
    print(f"Customer sales: {len(customer_sales):,}")
    print(f"Removed rows: {initial_rows - len(sales_clean):,}")
    print(f"Total revenue: £{sales_clean['Revenue'].sum():,.2f}")

    return sales_clean, customer_sales, quality_report