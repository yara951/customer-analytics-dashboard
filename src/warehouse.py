from sqlalchemy import create_engine, text

from src.config import BASE_DIR, DATABASE_URL


SQL_DIR = BASE_DIR / "sql"


def refresh_warehouse():

    print("Refreshing data warehouse...")

    engine = create_engine(DATABASE_URL)

    scripts = [
        "05_refresh_warehouse.sql",
        "06_refresh_rfm.sql"
    ]

    try:

        with engine.begin() as conn:

            for script in scripts:

                file_path = SQL_DIR / script

                sql_query = file_path.read_text(
                    encoding="utf-8"
                )

                conn.exec_driver_sql(sql_query)

                print(f"[EXECUTED] {script}")

            staging_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM public.retail_sales_staging
            """)).scalar_one()

            fact_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM public.fact_sales
            """)).scalar_one()

            customer_count = conn.execute(text("""
                SELECT COUNT(*)
                FROM public.customer_rfm
            """)).scalar_one()

            if staging_count == 0:
                raise ValueError("Staging table is empty")

            if staging_count != fact_count:
                raise ValueError("Sales row count mismatch")

            if customer_count == 0:
                raise ValueError("RFM table is empty")

            print(f"[PASS] Sales rows: {fact_count:,}")
            print(f"[PASS] RFM customers: {customer_count:,}")

        print("Data warehouse refreshed successfully.")

    finally:

        engine.dispose()