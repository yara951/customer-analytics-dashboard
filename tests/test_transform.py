import pandas as pd
import pytest

from src.transform import transform_data


@pytest.fixture
def sample_data():

    return pd.DataFrame({
        "InvoiceNo": ["1001", "1001", "C1002", "1003", "1004", "1005"],
        "StockCode": ["A", "A", "B", "C", "D", "E"],
        "Description": ["Product A", "Product A", "Product B",
                        "Product C", "Product D", "Product E"],
        "Quantity": [2, 2, -1, 0, 3, 4],
        "InvoiceDate": ["2011-01-01"] * 6,
        "UnitPrice": [10, 10, 5, 8, 0, 5],
        "CustomerID": [12345, 12345, 12346, 12347, 12348, None],
        "Country": ["United Kingdom"] * 6
    })


def test_remove_duplicates(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert not sales.duplicated().any()


def test_remove_cancellations(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert not sales["IsCancellation"].any()


def test_valid_quantities(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert (sales["Quantity"] > 0).all()


def test_valid_prices(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert (sales["UnitPrice"] > 0).all()


def test_revenue_calculation(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert sales["Revenue"].sum() == 40


def test_customer_sales(sample_data):

    _, customers, _ = transform_data(sample_data)

    assert customers["CustomerID"].notna().all()
    assert len(customers) == 1


def test_clean_sales_count(sample_data):

    sales, _, _ = transform_data(sample_data)

    assert len(sales) == 2