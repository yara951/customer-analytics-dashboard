import pandas as pd


def validate_data(sales_clean: pd.DataFrame,
                  customer_sales: pd.DataFrame):

    print("Validating data...")

    # Check empty datasets first
    if sales_clean.empty:
        raise ValueError("Sales dataset is empty")

    print("[PASS] Sales dataset is not empty")

    if customer_sales.empty:
        raise ValueError("Customer dataset is empty")

    print("[PASS] Customer dataset is not empty")

    # Data quality checks
    checks = {
        "No invalid quantities":
            sales_clean["Quantity"].gt(0).all(),

        "No invalid prices":
            sales_clean["UnitPrice"].gt(0).all(),

        "No cancelled invoices":
            not sales_clean["IsCancellation"].any(),

        "No missing invoice dates":
            sales_clean["InvoiceDate"].notna().all(),

        "No missing customer IDs in customer sales":
            customer_sales["CustomerID"].notna().all(),

        "No invalid revenue":
            sales_clean["Revenue"].gt(0).all()
    }

    for check, passed in checks.items():
        if not passed:
            raise ValueError(f"Validation failed: {check}")

        print(f"[PASS] {check}")

    print("All validation checks passed.")

    return True