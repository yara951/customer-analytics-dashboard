from time import perf_counter

from src.extract import extract_data
from src.transform import transform_data
from src.validation import validate_data
from src.load import load_to_postgresql
from src.warehouse import refresh_warehouse


def run_pipeline():

    start_time = perf_counter()

    print("=" * 50)
    print("ONLINE RETAIL - ETL PIPELINE")
    print("=" * 50)

    try:
        # Extract
        raw_data = extract_data()

        # Transform
        sales, customers, report = transform_data(raw_data)

        # Validate
        validate_data(sales, customers)

        # Load
        load_to_postgresql(sales)

        # Refresh Data Warehouse
        refresh_warehouse()

        elapsed_time = perf_counter() - start_time

        print("=" * 50)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Execution time: {elapsed_time:.2f} seconds")
        print("=" * 50)

    except Exception as error:
        print(f"Pipeline failed: {error}")
        raise


if __name__ == "__main__":
    run_pipeline()