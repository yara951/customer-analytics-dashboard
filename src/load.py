import pandas as pd
from src.config import PROCESSED_DIR
from sqlalchemy import create_engine, text
from src.config import DATABASE_URL


def save_processed_data(
    sales_clean: pd.DataFrame,
    customer_sales: pd.DataFrame,
    quality_report: pd.DataFrame
):

    print("Saving processed data...")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "sales_clean.csv": sales_clean,
        "customer_sales.csv": customer_sales,
        "data_quality_report.csv": quality_report
    }

    for filename, df in datasets.items():

        file_path = PROCESSED_DIR / filename

        df.to_csv(file_path, index=False)

        print(f"[SAVED] {filename} - {len(df):,} rows")

    print("Processed data saved successfully.")

def load_to_postgresql(sales_clean: pd.DataFrame):

    print("Loading data into PostgreSQL...")

    df = sales_clean.copy()

    # Normalize column names
    df.columns = df.columns.str.lower()

    engine = create_engine(DATABASE_URL)

    try:
        with engine.begin() as conn:

            df.to_sql(
                name="retail_sales_staging",
                con=conn,
                schema="public",
                if_exists="replace",
                index=False,
                chunksize=2000,
                method="multi"
            )

            row_count = conn.execute(
                text("SELECT COUNT(*) FROM public.retail_sales_staging")
            ).scalar_one()

            if row_count != len(df):
                raise ValueError("Row count mismatch")

            print(f"[LOADED] {row_count:,} rows")

        print("PostgreSQL load completed successfully.")

    finally:
        engine.dispose()